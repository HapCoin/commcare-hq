from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.core.management import BaseCommand
from django.core.management.base import CommandError
from django.urls import reverse

import io
import re

from dimagi.utils.csv import UnicodeWriter
from dimagi.utils.dates import DateSpan

from corehq.apps.accounting.models import BillingAccount, DefaultProductPlan, Subscription
from corehq.apps.app_manager.dbaccessors import get_brief_apps_in_domain
from corehq.apps.domain.models import Domain
from corehq.apps.es import forms as form_es
from corehq.apps.hqwebapp.tasks import send_html_email_async
from corehq.apps.reports.filters.users import ExpandedMobileWorkerFilter as EMWF
from corehq.apps.users.dbaccessors.all_commcare_users import get_all_user_rows, get_mobile_user_count
from corehq.apps.users.models import CouchUser, WebUser
from six.moves import map


class Command(BaseCommand):
    help = '''
        Generate three CSVs containing details on an enterprise project's domains, web users, and recent
        form submissions, respectively.

        Usage:
           report_on_enterprise_domain ACCOUNT_ID USERNAME
    '''

    def add_arguments(self, parser):
        parser.add_argument('account_id')
        parser.add_argument('username')

    def _domain_url(self, domain):
        return "https://www.commcarehq.org" + reverse('dashboard_domain', kwargs={'domain': domain})

    def _write_file(self, slug, timestamp, headers, process_domain, multiple=False):
        row_count = 0
        csv_file = io.BytesIO()
        writer = UnicodeWriter(csv_file)
        writer.writerow(headers)

        for domain in [domain.name for domain in map(Domain.get_by_name, self.domain_names) if domain]:
            result = process_domain(domain)
            rows = result if multiple else [result]
            row_count = row_count + len(rows)
            writer.writerows(rows)

        print('Wrote {} lines of {}'.format(row_count, slug))
        attachment = {
            'title': 'enterprise_{}_{}.csv'.format(slug, timestamp),
            'mimetype': 'text/csv',
            'file_obj': csv_file,
        }
        return (attachment, row_count)

    def _domain_row(self, domain):
        subscription = Subscription.get_active_subscription_by_domain(domain)
        plan_version = subscription.plan_version if subscription else DefaultProductPlan.get_default_plan_version()
        return [
            domain,
            self._domain_url(domain),
            plan_version.plan.name,
            str(get_mobile_user_count(domain, include_inactive=False)),
        ]

    def _web_user_row(self, domain):
        for user in get_all_user_rows(domain, include_web_users=True, include_mobile_users=False,
                                      include_inactive=False, include_docs=True):
            user = WebUser.wrap(user['doc'])
            return [
                user.full_name,
                user.username,
                user.role_label(domain),
                user.last_login.strftime(self.date_fmt),
                domain,
                self._domain_url(domain),
            ]

    def _form_row(self, domain):
        time_filter = form_es.submitted
        datespan = DateSpan(datetime.now() - timedelta(days=7), datetime.utcnow())
        apps = get_brief_apps_in_domain(domain)
        apps = {a.id: a.name for a in apps}
        users = get_all_user_rows(domain, include_web_users=False, include_mobile_users=True,
                                  include_inactive=False, include_docs=True)
        names = {}
        for user in users:
            user = user['doc']
            username = user['username']
            username = re.sub(r'@.*', '', username)
            names[username] = (user['first_name'], user['last_name'])
        users_filter = form_es.user_id(EMWF.user_es_query(domain,
                                       ['t__0'],  # All mobile workers
                                       self.couch_user)
                        .values_list('_id', flat=True))
        query = (form_es.FormES()
                 .domain(domain)
                 .filter(time_filter(gte=datespan.startdate,
                                     lt=datespan.enddate_adjusted))
                 .filter(users_filter))
        rows = []
        for hit in query.run().hits:
            username = hit['form']['meta']['username']
            submitted = datetime.strptime(hit['received_on'][:19], '%Y-%m-%dT%H:%M:%S').strftime(self.date_fmt)
            rows.append([
                hit['form']['@name'],
                submitted,
                apps[hit['app_id']] if hit['app_id'] in apps else 'App not found',
                domain,
                self._domain_url(domain),
                username,
                names[username][0] if username in names else 'User not found',
                names[username][1] if username in names else 'User not found',
            ])
        return rows

    def handle(self, account_id, username, **kwargs):
        self.date_fmt = '%Y/%m/%d %H:%M:%S'
        self.couch_user = CouchUser.get_by_username(username)
        if not self.couch_user:
            raise CommandError("Option: '--username' must be specified")

        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        account = BillingAccount.objects.get(id=account_id)
        subscriptions = Subscription.visible_objects.filter(account_id=account.id, is_active=True)
        self.domain_names = set(s.subscriber.domain for s in subscriptions)
        print('Found {} domains for {}'.format(len(self.domain_names), account.name))

        headers = ['Project Space Name', 'Project Space URL', 'Project Space Plan', '# of mobile workers']
        (domain_file, domain_count) = self._write_file('domains', timestamp, headers, self._domain_row)

        headers = ['Name', 'Email Address', 'Role', 'Last Login', 'Project Space Name', 'Project Space URL']
        (web_user_file, web_user_count) = self._write_file('web_users', timestamp, headers, self._web_user_row)

        headers = ['Form Name', 'Submitted', 'App Name', 'Project Space Name', 'Project Space URL',
                   'Mobile User', 'First Name', 'Last Name']
        (form_file, form_count) = self._write_file('forms', timestamp, headers, self._form_row, multiple=True)

        message = (
            '''
                Domains: {}\n
                Web Users: {}\n
                Forms: {}\n
            '''.format(domain_count, web_user_count, form_count)
        )

        send_html_email_async(
            "Report on enterprise domain", self.couch_user.username, message,
            text_content=message, file_attachments=[
                domain_file,
                web_user_file,
                form_file,
            ]
        )
        print('Emailed {}'.format(self.couch_user.username))
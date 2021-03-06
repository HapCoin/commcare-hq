from __future__ import absolute_import
from __future__ import unicode_literals
from corehq.preindex import ExtraPreindexPlugin
from django.conf import settings

ExtraPreindexPlugin.register('domain', __file__, (
    settings.NEW_DOMAINS_DB,
    settings.NEW_USERS_GROUPS_DB,
    settings.NEW_FIXTURES_DB,
    'meta',
))

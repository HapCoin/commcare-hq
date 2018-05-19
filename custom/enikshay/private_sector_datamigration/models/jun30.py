from __future__ import absolute_import
from django.db import models


class Agency_Jun30(models.Model):
    id = models.IntegerField(null=True, unique=True)
    agencyId = models.IntegerField(primary_key=True)
    agencyName = models.CharField(max_length=256, null=True)
    agencyStatus = models.CharField(max_length=256, null=True)
    agencySubTypeId = models.CharField(max_length=256, null=True)
    agencyTypeId = models.CharField(max_length=256)
    associatedFOId = models.CharField(max_length=256, null=True)
    attachedToAgency = models.CharField(max_length=256, null=True)
    creationDate = models.DateTimeField()
    creator = models.CharField(max_length=256, null=True)
    dateOfRegn = models.DateTimeField()
    labOrLcc = models.CharField(max_length=256, null=True)
    modificationDate = models.DateTimeField()
    modifiedBy = models.CharField(max_length=256, null=True)
    nikshayId = models.CharField(max_length=256, null=True)
    nikshayProcessedFlag = models.CharField(max_length=1, null=True)
    onBehalfOf = models.CharField(max_length=256, null=True)
    organisationId = models.IntegerField()
    owner = models.CharField(max_length=256, null=True)
    parentAgencyId = models.IntegerField()
    parentAgencyType = models.CharField(max_length=256, null=True)
    payToParentAgency = models.CharField(max_length=256, null=True)
    pendingApproval = models.CharField(max_length=256, null=True)
    regnIssueAuthId = models.CharField(max_length=256, null=True)
    regnNumber = models.CharField(max_length=256, null=True)
    sendAlert = models.CharField(max_length=256, null=True)
    subOrganisationId = models.IntegerField()
    tbDrugInStock = models.CharField(max_length=256, null=True)
    tbTests = models.CharField(max_length=256, null=True)
    trainingAttended = models.CharField(max_length=256, null=True)
    tbCorner = models.CharField(max_length=1, null=True)


class UserDetail_Jun30(models.Model):
    id = models.IntegerField(primary_key=True)
    accountTypeId = models.CharField(max_length=256, null=True)
    addressLineOne = models.CharField(max_length=256, null=True)
    addressLineTwo = models.CharField(max_length=256, null=True)
    agencyId = models.IntegerField()
    alternateMobileNumber = models.CharField(max_length=256, null=True)
    alternateMobileNumber1 = models.CharField(max_length=256, null=True)
    alternateMobileNumber2 = models.CharField(max_length=256, null=True)
    bankAccountName = models.CharField(max_length=256, null=True)
    bankAccountNumber = models.CharField(max_length=256, null=True)
    bankBranch = models.CharField(max_length=256, null=True)
    bankIFSCCode = models.CharField(max_length=256, null=True)
    bankName = models.CharField(max_length=256, null=True)
    blockOrHealthPostId = models.CharField(max_length=256, null=True)
    creationDate = models.DateTimeField(null=True)
    creator = models.CharField(max_length=256, null=True)
    districtId = models.CharField(max_length=256, null=True)
    dob = models.DateTimeField(null=True)
    email = models.CharField(max_length=256, null=True)
    firstName = models.CharField(max_length=256, null=True)
    gender = models.CharField(max_length=256, null=True)
    isPasswordResetFlag = models.NullBooleanField()
    isPrimary = models.BooleanField()
    landLineNumber = models.CharField(max_length=256, null=True)
    lastName = models.CharField(max_length=256, null=True)
    latitude = models.CharField(max_length=256, null=True)
    longitude = models.CharField(max_length=256, null=True)
    micrCode = models.IntegerField(null=True)
    middleName = models.CharField(max_length=256, null=True)
    mobileNumber = models.CharField(max_length=256, null=True)
    modificationDate = models.DateTimeField(null=True)
    modifiedBy = models.CharField(max_length=256, null=True)
    motechUserName = models.CharField(max_length=256, unique=True)
    organisationId = models.IntegerField()
    owner = models.CharField(max_length=256, null=True)
    passwordResetFlag = models.BooleanField()
    pincode = models.IntegerField()
    stateId = models.CharField(max_length=256, null=True)
    status = models.CharField(max_length=256, null=True)
    subOrganisationId = models.IntegerField()
    tuId = models.CharField(max_length=256, null=True)
    uniqIDNo = models.CharField(max_length=256, null=True)
    uniqIDType = models.CharField(max_length=256, null=True)
    userId = models.IntegerField()
    userName = models.CharField(max_length=256, null=True)
    valid = models.BooleanField()
    villageTownCity = models.CharField(max_length=256, null=True)
    wardId = models.CharField(max_length=256, null=True)
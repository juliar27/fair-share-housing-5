from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


# ----------------------------------------------------------------------------------------------------------------------
class LoginForm(FlaskForm):
    municode = StringField('Municode')
    municipality = StringField('Municipality')
    county = StringField('County')
    region = StringField('Region')
    name = StringField('Site Program Name')
    developer = StringField('Project Developer')
    compliance = StringField('Compliance Mechanism')
    address = StringField('Address')
    status = StringField('Status')
    total = StringField('Total # Overall Units')
    family = StringField('Total # Family Units')
    famsale = StringField('# Family Units for Sale')
    famrent = StringField('# Family Units for Rent')
    senior = StringField('Total # Senior Units')
    srsale = StringField('# Senior Units for Sale')
    srrent = StringField('# Senior Units for Rent')
    ssn = StringField('Total # SSN Units')
    ssnsale = StringField('# SSN Units for Sale')
    ssnrent = StringField('# SSN Units for Rent')
    v1 = StringField('# Very Low Income 1 Bedroom Units')
    l1 = StringField('# Low Income 1 Bedroom Units')
    m1 = StringField('# Moderate Income 1 Bedroom Units')

    v2 = StringField('# Very Low Income 2 Bedroom Units')
    l2 = StringField('# Low Income 2 Bedroom Units')
    m2 = StringField('# Moderate Income 2 Bedroom Units')

    v3 = StringField('# Very Low Income 3+ Bedroom Units')
    l3 = StringField('# Low Income 3+ Bedroom Units')
    m3 = StringField('# Moderate Income 3+ Bedroom Units')

    vssn = StringField('# Very Low Income SSN Units')
    lssn = StringField('# Low Income SSN Units')
    mssn = StringField('# Moderate Income SSN Units')

    br1 = StringField('Total # 1 Bedroom Units')
    br2 = StringField('Total # 2 Bedroom Units')
    br3 = StringField('Total # 3 Bedroom Units')
    submit = SubmitField('Submit')
# ----------------------------------------------------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


# ----------------------------------------------------------------------------------------------------------------------
class AddForm(FlaskForm):
    municode = StringField('Municode')
    muni = StringField('Municipality')
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
    vli1 = StringField('# Very Low Income 1 Bedroom Units')
    li1 = StringField('# Low Income 1 Bedroom Units')
    m1 = StringField('# Moderate Income 1 Bedroom Units')

    vli2 = StringField('# Very Low Income 2 Bedroom Units')
    li2 = StringField('# Low Income 2 Bedroom Units')
    m2 = StringField('# Moderate Income 2 Bedroom Units')

    vli3 = StringField('# Very Low Income 3+ Bedroom Units')
    li3 = StringField('# Low Income 3+ Bedroom Units')
    m3 = StringField('# Moderate Income 3+ Bedroom Units')

    vssn = StringField('# Very Low Income SSN Units')
    lssn = StringField('# Low Income SSN Units')
    mssn = StringField('# Moderate Income SSN Units')

    total1 = StringField('Total # 1 Bedroom Units')
    total2 = StringField('Total # 2 Bedroom Units')
    total3 = StringField('Total # 3 Bedroom Units')
    submit = SubmitField('Submit')
# ----------------------------------------------------------------------------------------------------------------------


from django.forms import ModelForm, Form, FileField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Fieldset, Hidden, Field
from crispy_forms.bootstrap import FormActions, AppendedPrependedText, AppendedText
from drss.models import Project, Payment, Comment, Document


class NewApplication(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewApplication, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            Fieldset(
                'Store Details',
                'concept',
                AppendedText('store_size', 'SQFT'),
                'sales_rep',
                'advertising_source',
                Field('opening_location', placeholder="City,ST"),
            ),
            Fieldset(
                'Contact Information',
                'first_name',
                'last_name',
                'email',
                'social_security',
                Field('date_of_birth', placeholder="yyyy-mm-dd"),
                Field('home_phone', placeholder="xxx-xxx-xxxx"),
                Field('cell_phone', placeholder="xxx-xxx-xxxx"),
                Field('fax_number', placeholder="xxx-xxx-xxxx"),
                'best_call_time',
                'address',
                'city',
                'state',
                'zip_code',

            ),
            Fieldset(
                'Partner Information',
                HTML("<div class='alert alert-info'>Complete the following section if you are appyling with a spouse or business partner. To request a partner, check below.</div>"),
                'needs_partner',
                'first_name_partner',
                'last_name_partner',
                'email_partner',
                'social_security_partner',
                Field('date_of_birth_partner', placeholder="yyyy-mm-dd"),
                Field('home_phone_partner', placeholder="xxx-xxx-xxxx"),
                Field('cell_phone_partner', placeholder="xxx-xxx-xxxx"),
                Field('fax_number_partner', placeholder="xxx-xxx-xxxx"),
                'address_partner',
                'city_partner',
                'state_partner',
                'zip_code_partner',

            ),
            Fieldset(
                'Credit and Employment',
                'place_of_employment',
                'place_of_employment_partner',
                'years_at_job',
                'years_at_job_partner',
                'annual_salary',
                'annual_salary_partner',
                'credit_score',
                'credit_score_partner'

            ),
            Fieldset(
                'Funds Available',
                HTML("<div class='alert alert-info'>Enter assets you have available and may wish to consider for use in funding your store.</div>"),
                AppendedPrependedText('financing_cash', '$', '.00'),
                AppendedPrependedText('financing_loc', '$', '.00'),
                AppendedPrependedText('financing_hloc', '$', '.00'),
                AppendedPrependedText('financing_401k', '$', '.00'),
                AppendedPrependedText('financing_pension', '$', '.00'),
                AppendedPrependedText('financing_ira', '$', '.00'),
                AppendedPrependedText('financing_stocksbonds', '$', '.00'),
                AppendedPrependedText('financing_cd', '$', '.00'),
                AppendedPrependedText('financing_lifeinsurance', '$', '.00'),

            ),
            Fieldset(
                'Terms and Application Agreement',
                HTML("<p>My signature below authorizes: Dollar Store Services to obtain my consumer credit report and verifies that I am releasing my financial information including ACH Authorization to Dollar Store Services. It is understood and agreed that this deposit is 100% refundable if the proper location for a store is not found and / or financing cannot be secured. With your prior approval, we will send a representative to do site location for you in your area. Only in that instance will reasonable travel expenses be deducted from your deposit amount. Once work begins in Real Estate on your project, the Company will be expending considerable resources to identify, evaluate and negotiate the lease terms of locations that you approve. It is imperative that you remain in constant contact with your leasing team, as time is of the essence in securing a location. You may request that your project be put on hold (for example, due to a family vacation or personal emergency) at any time, without penalty. A lapse of more than 7 days in telephone communication will result in the forfeiture of $1,500 of your deposit. More importantly, it may result in the loss of a desired store location. It is important that the net worth be realistic so we research the proper size of store that fits your budget.</p>"),
                Field('signature', placeholder="Type Full Name Here")
            ),
            Hidden('deposit_amount', '1500'),
            Hidden('package_price', '0'),
            Hidden('status', '1'),
            Hidden('submission_ip', '127.0.0.1'),
            HTML("<div class='alert alert-info'>After signing your application, you will be asked to submit your fully refundable deposit, remember your application is not complete until your deposit amount is received. Ask your National Development Director if you have any questions.</div>"),
            FormActions(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

    class Meta:
        model = Project


class NewDeposit(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewDeposit, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            Fieldset('Receive Deposit', 'payment_amount', 'payment_type', 'trace_number', 'last_four_num', 'project', 'hold'),
            FormActions(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

    class Meta:
        model = Payment


class FileUpload(Form):
    docfile = FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


class SalesApplication(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalesApplication, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            Fieldset(
                'Store Details',
                'concept',
                AppendedText('store_size', 'SQFT'),
                'sales_rep',
                'advertising_source',
                Field('opening_location', placeholder="City,ST"),
            ),
            Fieldset(
                'Contact Information',
                'first_name',
                'last_name',
                'email',
                'social_security',
                Field('date_of_birth', placeholder="yyyy-mm-dd"),
                Field('home_phone', placeholder="xxx-xxx-xxxx"),
                Field('cell_phone', placeholder="xxx-xxx-xxxx"),
                Field('fax_number', placeholder="xxx-xxx-xxxx"),
                'best_call_time',
                'address',
                'city',
                'state',
                'zip_code',

            ),
            Fieldset(
                'Partner Information',
                HTML("<div class='alert alert-info'>Complete the following section if you are appyling with a spouse or business partner. To request a partner, check below.</div>"),
                'needs_partner',
                'first_name_partner',
                'last_name_partner',
                'email_partner',
                'social_security_partner',
                Field('date_of_birth_partner', placeholder="yyyy-mm-dd"),
                Field('home_phone_partner', placeholder="xxx-xxx-xxxx"),
                Field('cell_phone_partner', placeholder="xxx-xxx-xxxx"),
                Field('fax_number_partner', placeholder="xxx-xxx-xxxx"),
                'address_partner',
                'city_partner',
                'state_partner',
                'zip_code_partner',

            ),
            Fieldset(
                'Credit and Employment',
                'place_of_employment',
                'place_of_employment_partner',
                'years_at_job',
                'years_at_job_partner',
                'annual_salary',
                'annual_salary_partner',
                'credit_score',
                'credit_score_partner'

            ),
            Fieldset(
                'Funds Available',
                HTML("<div class='alert alert-info'>Enter assets you have available and may wish to consider for use in funding your store.</div>"),
                AppendedPrependedText('financing_cash', '$', '.00'),
                AppendedPrependedText('financing_loc', '$', '.00'),
                AppendedPrependedText('financing_hloc', '$', '.00'),
                AppendedPrependedText('financing_401k', '$', '.00'),
                AppendedPrependedText('financing_pension', '$', '.00'),
                AppendedPrependedText('financing_ira', '$', '.00'),
                AppendedPrependedText('financing_stocksbonds', '$', '.00'),
                AppendedPrependedText('financing_cd', '$', '.00'),
                AppendedPrependedText('financing_lifeinsurance', '$', '.00'),

            ),
            Hidden('deposit_amount', '1500'),
            Hidden('package_price', '0'),
            Hidden('submission_ip', '127.0.0.1'),
            Hidden('status', '1'),
            HTML("<div class='alert alert-info'>After signing your application, you will be asked to submit your fully refundable deposit, remember your application is not complete until your deposit amount is received. Ask your National Development Director if you have any questions.</div>"),
            FormActions(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

    class Meta:
        model = Project

import os.path
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.localflavor.us.us_states import STATE_CHOICES
# Create your models here.


class Concept(models.Model):
    title = models.CharField(max_length=100)
    achdirect_api_key = models.CharField(max_length=100, blank=True)
    achdirect_secure_key = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.title


class Status(models.Model):
    title = models.CharField(max_length=100)
    weight = models.IntegerField()

    def __unicode__(self):
        return self.title


class PackageOption(models.Model):
    title = models.CharField(max_length=100)
    amount = models.IntegerField()
    concept = models.ForeignKey(Concept)

    def __unicode__(self):
        return self.title


class Department(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title


class Employee(models.Model):
    user = models.OneToOneField(User)

    def full_name(self):
        name = self.user.last_name + ", " + self.user.first_name
        return name

    def __unicode__(self):
        name = self.user.last_name + ", " + self.user.first_name
        return name


class SalesPerson(Employee):
    concept = models.ForeignKey(Concept)

    def working_projects(self):
        projects = self.projects_set.all()
        project_count = 0
        for project in projects:
            project_count = project_count + 1
        return project_count
    working_projects.admin_order_field = 'working_projects'
    working_projects.boolean = False
    working_projects.short_description = 'Number of Clients in Finance'


class FinanceAdvisor(Employee):
    credit_repair = models.BooleanField()


class AdvertisingSource(models.Model):
    campaign = models.CharField(max_length=64)

    def __unicode__(self):
        return self.campaign

    class Meta:
        ordering = ('campaign',)


class Project(models.Model):
    MORNING = 'Morning'
    AFTERNOON = 'SO'
    EVENING = 'Evening'
    TIME_TO_CALL_CHOICES = (
        (MORNING, 'Morning'),
        (AFTERNOON, 'Afternoon'),
        (EVENING, 'Evening'),
    )
    create_date = models.DateTimeField('Date Created', auto_now_add=True)
    concept = models.ForeignKey(Concept, verbose_name="Store Concept",  help_text="Your preferred retail concept.")
    status = models.ForeignKey(Status, verbose_name="Status", null=True, blank=True)
    refund_date = models.DateField('Refund Date', null=True, blank=True)
    sales_rep = models.ForeignKey(SalesPerson,  related_name='assigned_sales_rep', verbose_name="Development Director")
    customers_user = models.ForeignKey(User,  related_name='customers_user', verbose_name="Customers User", null=True, blank=True)
    funding_advisor = models.ForeignKey(FinanceAdvisor, related_name='assigned_funding_advisor', null=True, blank=True, verbose_name="Funding Advisor")
    needs_partner = models.BooleanField("Request a Partner")
    store_size = models.IntegerField("Store Square Footage", null=True)
    package_price = models.DecimalField("Package Price", max_digits=10, decimal_places=2)
    advertising_source = models.ForeignKey(AdvertisingSource,  verbose_name="Where did you hear about us?")
    opening_location = models.CharField("Store Location", max_length=64)
    package_price = models.DecimalField("Package Price", max_digits=10, decimal_places=2, blank=True)
    deposit_amount = models.DecimalField("Store Deposit Amount", max_digits=10, decimal_places=2, blank=True, default=1500)
    financing_cash = models.DecimalField("Cash Funds", max_digits=10, decimal_places=2)
    financing_loc = models.DecimalField("Line of Credit", max_digits=10, decimal_places=2)
    financing_hloc = models.DecimalField("Home Equity LOC", max_digits=10, decimal_places=2)
    financing_401k = models.DecimalField("401K Funds", max_digits=10, decimal_places=2)
    financing_pension = models.DecimalField("Pension Funds", max_digits=10, decimal_places=2)
    financing_ira = models.DecimalField("IRA Funds", max_digits=10, decimal_places=2)
    financing_stocksbonds = models.DecimalField("Stocks and Bonds", max_digits=10, decimal_places=2)
    financing_cd = models.DecimalField("CD Funds", max_digits=10,  decimal_places=2)
    financing_lifeinsurance = models.DecimalField("Life Insurance", max_digits=10, decimal_places=2)
    first_name = models.CharField("First Name", max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField("E-Mail")
    social_security = models.CharField("Social Security Number", max_length=32)
    address = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField('Date of Birth')
    best_call_time = models.CharField('Best Time to Call', max_length=32, choices=TIME_TO_CALL_CHOICES, default=MORNING)
    home_phone = models.CharField('Primary Phone', max_length=32, null=True)
    cell_phone = models.CharField('Cell Phone', max_length=32, null=True, blank=True)
    fax_number = models.CharField('Fax Number', max_length=32, null=True, blank=True)
    credit_score = models.IntegerField('Credit Score')
    place_of_employment = models.CharField('Place of Employment', max_length=128)
    years_at_job = models.IntegerField('Years at Job', )
    annual_salary = models.IntegerField('Annual Salary', )
    first_name_partner = models.CharField("Partner's Last Name", max_length=32, null=True, blank=True)
    last_name_partner = models.CharField("Partner's First Name", max_length=32, null=True, blank=True)
    email_partner = models.EmailField("Partner's Email", null=True, blank=True)
    social_security_partner = models.CharField("Partner's SSN", max_length=32, null=True, blank=True)
    address_partner = models.CharField("Partner's Address", max_length=64, null=True, blank=True)
    city_partner = models.CharField("Partner's City", max_length=32, null=True, blank=True)
    state_partner = models.CharField("Partner's State", max_length=2, null=True, blank=True, choices=STATE_CHOICES)
    zip_code_partner = models.CharField("Partner's Zip Code", max_length=10, null=True, blank=True)
    date_of_birth_partner = models.DateField("Partner's Date of Birth",  null=True, blank=True)
    best_call_time_partner = models.CharField("Partner's Best Time to Call", max_length=32, null=True, blank=True)
    home_phone_partner = models.CharField("Partner's Home Phone", max_length=32, null=True, blank=True)
    cell_phone_partner = models.CharField("Partner's Cell Phone Number", max_length=32, null=True, blank=True)
    fax_number_partner = models.CharField("Partner's Fax Number", max_length=32, null=True, blank=True)
    credit_score_partner = models.IntegerField("Partner's Credit Score", null=True, blank=True)
    place_of_employment_partner = models.CharField("Partner's Place of Employment", max_length=128, null=True, blank=True)
    years_at_job_partner = models.IntegerField("Partner's Years at Job", null=True, blank=True)
    annual_salary_partner = models.IntegerField("Partner's Salary", null=True, blank=True)
    signature = models.CharField("Signature", max_length=100, default="", null=True, blank=True)

    def is_paid(self):
        payments = self.payment_set.all()
        if payments:
            if payments[0].bounce:
                return 3
            else:
                return 1
        else:
            return 2
    is_paid.admin_order_field = 'is_paid'
    is_paid.boolean = False
    is_paid.short_description = 'Has Deposit Been Paid?'

    def doc_list(self):
        documents = self.document_set.all()
        document_list = ""
        for document in documents:
            if not bool(document.document_file):
                document_list = document_list + document.title + ", "
        if len(document_list) == 0:
            return False
        else:
            return document_list

    def payment_info(self):
        payments = self.payment_set.all()
        if payments:
            payment = payments[0]
            payment_date = payment.payment_date.strftime('%m/%d/%y')
            return payment_date
        else:
            return "No Payment."
    payment_info.admin_field = 'payment_info'
    payment_info.boolean = False
    payment_info.short_description = 'Payment Info'

    def completion(self):
        percent = 25
        status = 'danger'
        if self.is_paid() == 1:
            percent = percent + 25
            status = 'warning'
            if not self.doc_list():
                percent = percent + 50
                status = 'success'
                return {'percent': percent, 'status': status}
        if self.doc_list():
            doc_factor = len(self.doc_list())
        else:
            doc_factor = 0
        document_progress = 50 - doc_factor
        percent = percent + document_progress
        docs = self.document_set.all()
        for doc in docs:
            if doc.internal is True and bool(doc.document_file) is False:
                status = 'danger'
        return {'percent': percent, 'status': status}

    def full_name(self):
        full_name = self.first_name + " " + self.last_name
        return full_name

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        is_new = self.id is None
        super(Project, self).save(*args, **kwargs)
        if is_new:
            Document.objects.create(project=self, title='Act Notes', internal=True)
            Document.objects.create(project=self, title='SRTO', internal=True)
            if self. financing_cash > 0:
                Document.objects.create(project=self, title='Cash')
            if self.financing_hloc > 0:
                Document.objects.create(project=self, title='HLOC')
            if self.financing_401k > 0:
                Document.objects.create(project=self, title='401K')
            if self.financing_pension > 0:
                Document.objects.create(project=self, title='Pension')
            if self.financing_ira > 0:
                Document.objects.create(project=self, title='IRA')
            if self.financing_stocksbonds > 0:
                Document.objects.create(project=self, title='Stocks and Bonds')
            if not User.objects.filter(username=self.email).count():
                user = User.objects.create_user(self.email, self.email, 'erF213')
                user.last_name = self.last_name
                user.first_name = self.first_name
                user.save()
                self.customers_user = user
                self.save()
            id = str(self.id)
            subject = "A new DRSS Store Application has Been Created for You"
            message = "To Complete your Application and pay your deposit. Please visit https://finance.drssone.com/application/"+id+"/ You may login with username:"+self.email+" and password: erX613"
            to_address = [self.email]
            send_mail(subject, message, 'deposits@drssmail.com', to_address, fail_silently=False)

    def __unicode__(self):
        full_name = self.last_name + ", " + self.first_name
        return full_name


class Payment(models.Model):
    CC = 'Credit Card'
    CHK = 'Check'
    CCHK = 'Cashiers Check'
    CASH = 'Cash'
    PAYMENT_TYPE_CHOICES = (
        (CC, 'Credit Card'),
        (CHK, 'Check'),
        (CCHK, 'Cashiers Check'),
        (CASH, 'Cash')
    )
    payment_amount = models.DecimalField(max_digits=10,  decimal_places=2)
    payment_date = models.DateTimeField('Deposit Date', auto_now_add=True)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_TYPE_CHOICES)
    bounce = models.BooleanField('Has Bounced', default=False)
    trace_number = models.CharField(max_length=100)
    last_four_num = models.CharField(max_length=100)
    project = models.ForeignKey(Project)
    hold = models.DateTimeField('Hold to Date', null=True, blank=True)

    def __unicode__(self):
        return self.payment_type


class Comment(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User)
    post_date = models.DateTimeField('date requested', auto_now_add=True)
    internal = models.BooleanField()
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return self.body


class DocumentType(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Document(models.Model):
    title = models.CharField(max_length=100)
    project = models.ForeignKey(Project)
    internal = models.BooleanField(blank=True, default=False)
    request_date = models.DateTimeField('date requested', auto_now_add=True)
    submit_date = models.DateTimeField('submit date', null=True, blank=True, auto_now=True)
    submission_ip = models.IPAddressField(null=True, blank=True)
    document_file = models.FileField(upload_to="documents", null=True, blank=True)

    def filename(self):
        return os.path.basename(self.document_file.name)

    def isCompleted(self):
        if bool(self.document_file) is False:
            return False
        else:
            return True

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('request_date',)

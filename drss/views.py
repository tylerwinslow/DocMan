from django.shortcuts import render
import re
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from rest_framework import generics
from django_easyfilters import FilterSet
from drss.models import Project, Comment, Document, Payment, DocumentType, FinanceAdvisor, Status, SalesPerson, ShoppingCenter
from task_manager.models import Task
from drss.forms import NewApplication, NewDeposit, FileUpload, SalesApplication, CreateSite
from drss.serializers import CommentSerializer, DocumentSerializer, PaymentSerializer, ProjectSerializer, UserSerializer, StatusSerializer


def check_group(user, groupcheck):
    groups = user.groups.values_list('name', flat=True)
    for group in groups:
        if group == groupcheck:
            return True
    return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ProjectFilterSet(FilterSet):
    fields = [
        'create_date',
        'concept',
        'status',
        'sales_rep',
        'funding_advisor'

    ]


class PaymentFilterSet(FilterSet):
    fields = [
        'payment_date',
    ]


def api_root(request):
    return HttpResponseRedirect('/projects')


def application(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = NewApplication(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            new_app = form.save(commit=False)
            new_app.submission_ip = get_client_ip(request)
            new_app.home_phone = re.sub("[^0-9]", "", new_app.home_phone)
            new_app.save()
            return HttpResponseRedirect(reverse('drss.views.deposit', args=(new_app.id,)))  # Redirect after POST
    else:
        form = NewApplication()  # An unbound form

    return render(request, 'application.html', {
        'form': form,
    })


def application_detail(request, app_id):
    if request.user.is_authenticated():
    # Do something for authenticated users.
        app = Project.objects.get(pk=app_id)
        if request.method == 'POST':  # If the form has been submitted...
            form = NewApplication(request.POST, instance=app)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                new_app = form.save(commit=False)
                new_app.submission_ip = get_client_ip(request)
                new_app.home_phone = re.sub("[^0-9]", "", new_app.home_phone)
                new_app.save()
                return HttpResponseRedirect(reverse('drss.views.deposit', args=(app_id,)))  # Redirect after POST
        else:
            form = NewApplication(instance=app)  # Load Form for Verification
        if not app.signature:
            return render(request, 'application.html', {
                'form': form,
            })
        else:
            return HttpResponseRedirect(reverse('drss.views.deposit', args=(app_id,)))
    else:
        return render(request, 'not-authenticated.html')


def deposit(request, app_id):
        project = Project.objects.get(pk=app_id)
        if project.is_paid() == 2:
            secret_key = project.concept.achdirect_api_key
            amount = project.deposit_amount
            last_name = project.last_name
            first_name = project.first_name
            address = project.address
            city = project.city
            state = project.state
            zip_code = project.zip_code
            home_phone = project.home_phone
            email = project.email
            context = {"customer_id": app_id, "secret_key": secret_key, "amount": amount,
                       "last_name": last_name, "first_name": first_name, "address": address, "city": city, "state": state, "zip_code": zip_code,
                       "home_phone": home_phone, "email": email,
                       }
            return render(request, 'payment.html', context)
        else:
            return render(request, 'paid.html')


def submit_docs(request, app_id):
    if request.user.is_authenticated():
        project = Project.objects.get(pk=app_id)
        documents = project.document_set.filter(internal=False)
        context = {'documents': documents}
        return render(request, 'documents.html', context)
    else:
        return render(request, 'not-authenticated.html')


def print_app(request, app_id):
    project = Project.objects.get(pk=app_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="application.pdf"'
    p = SimpleDocTemplate(response, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    template = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=6))
    ptext = "%s Store Application" % (project.concept)
    template.append(Paragraph(ptext, styles["Normal"]))
    template.append(Spacer(1, 12))
    ptext = "%s,%s" % (project.last_name, project.first_name)
    template.append(Paragraph(ptext, styles["Normal"]))
    template.append(Paragraph(project.address, styles["Normal"]))
    ptext = "%s,%s %s" % (project.city, project.state, project.zip_code)
    template.append(Paragraph(ptext, styles["Normal"]))
    template.append(Spacer(1, 24))
    ptext = "Store Details"
    template.append(Paragraph(ptext, styles["Normal"]))
    ptext = "Store Concept: %s" % (project.concept)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Store Square Footage: %s" % (project.store_size)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Development Director: %s" % (project.sales_rep)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Where did you hear about us?: %s" % (project.advertising_source)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Store Location: %s" % (project.opening_location)
    template.append(Paragraph(ptext, styles["Justify"]))
    template.append(Spacer(1, 24))
    ptext = "Contact Information"
    template.append(Paragraph(ptext, styles["Normal"]))
    ptext = "First Name: %s" % (project.first_name)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Last Name: %s" % (project.last_name)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "E-Mail: %s" % (project.email)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Social Security Number: %s" % (project.social_security)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Date of Birth: %s" % (project.date_of_birth)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Primary Phone: %s" % (project.home_phone)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Cell Phone: %s" % (project.cell_phone)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Fax Number: %s" % (project.fax_number)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Best Time to Call: %s" % (project.best_call_time)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Address: %s" % (project.address)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "City: %s" % (project.city)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "State: %s" % (project.state)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Zip Code: %s" % (project.zip_code)
    template.append(Paragraph(ptext, styles["Justify"]))
    template.append(Spacer(1, 24))
    ptext = "Partner Information"
    template.append(Paragraph(ptext, styles["Normal"]))
    ptext = "Partner's Last Name: %s" % (project.last_name_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's First Name: %s" % (project.first_name_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's E-Mail: %s" % (project.email_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's SSN: %s" % (project.social_security_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's Date of Birth: %s" % (project.date_of_birth_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's Home Phone: %s" % (project.home_phone_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's Cell Phone Number: %s" % (project.cell_phone_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's Fax Number: %s" % (project.fax_number_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's Address: %s" % (project.address_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's City: %s" % (project.city_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's State: %s" % (project.state_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's Zip Code: %s" % (project.zip_code_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Credit and Employment" 
    template.append(Spacer(1, 24))
    template.append(Paragraph(ptext, styles["Normal"]))
    ptext = "Place of Employment: %s" % (project.place_of_employment)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's Place of Employment: %s" % (project.place_of_employment_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Years at Job: %s" % (project.years_at_job)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's Years at Job: %s" % (project.years_at_job_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Annual Salary: %s" % (project.annual_salary)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's Annual Salary: %s" % (project.annual_salary_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Credit Score: %s" % (project.credit_score)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Partner's Credit Score: %s" % (project.credit_score_partner)
    template.append(Paragraph(ptext, styles["Justify"]))
    template.append(Spacer(1, 48))
    ptext = "Funds Available"
    template.append(Paragraph(ptext, styles["Normal"]))
    ptext = "Cash Funds: %s" % (project.financing_cash)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Line of Credit: %s" % (project.financing_loc)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Home Equity LOC: %s" % (project.financing_hloc)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "401K Funds: %s" % (project.financing_401k)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Pension Funds: %s" % (project.financing_pension)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "IRA Funds: %s" % (project.financing_ira)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Stocks and Bonds: %s" % (project.financing_stocksbonds)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "CD Funds: %s" % (project.financing_cd)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Life Insurance: %s" % (project.financing_lifeinsurance)
    template.append(Paragraph(ptext, styles["Justify"]))
    template.append(Spacer(1, 36))
    template.append(Paragraph("Signature", styles["Normal"]))
    ptext = "My signature below authorizes: %s to obtain my consumer credit report and verifies that I am releasing my financial information including ACH Authorization. It is understood and agreed that this deposit is 100 percent refundable if the proper location for a store is not found and / or financing cannot be secured. With your prior approval, we will send a representative to do site location for you in your area. Only in that instance will reasonable travel expenses be deducted from your deposit amount. Once work begins in Real Estate on your project, the Company will be expending considerable resources to identify, evaluate and negotiate the lease terms of locations that you approve. It is imperative that you remain in constant contact with your leasing team, as time is of the essence in securing a location. You may request that your project be put on hold (for example, due to a family vacation or personal emergency) at any time, without penalty. A lapse of more than 7 days in telephone communication will result in the forfeiture of $1,500 of your deposit. More importantly, it may result in the loss of a desired store location. It is important that the net worth be realistic so we research the proper size of store that fits your budget." % (project.concept)
    template.append(Paragraph(ptext, styles["Justify"]))
    ptext = "Signature: %s" % (project.signature)
    template.append(Paragraph(ptext, styles["Normal"]))

    p.build(template)
    return response


def thankyou(request):
    return render(request, 'thankyou.html')


def support(request):
    return render(request, 'support.html')


@csrf_exempt
def payment_complete(request):
    customer_id = request.REQUEST["pg_merchant_data_1"]
    project = Project.objects.get(pk=customer_id)
    payment = Payment(payment_amount='1500', payment_type='Credit Card', trace_number='1555', last_four_num='5555', project=project)
    payment.save()
    context = {'customer_id': customer_id}
    return render(request, 'receipt.html', context)


def project_list(request):
    if request.user.is_authenticated() and request.user.is_staff:
        group = request.user.groups.values_list('name', flat=True)
        the_filter = request.user.username
        if group:
            if group[0] == "Sales Person":
                sales_filter = request.user.username
                projects = Project.objects.filter(sales_rep__user__username__startswith=sales_filter).order_by('-create_date')
            elif group[0] == "Funding Advisor":
                funding_filter = request.user.username
                projects = Project.objects.filter(funding_advisor__user__username__startswith=funding_filter).exclude(assignment_date__isnull=True).order_by('-assignment_date')
            else:
                projects = Project.objects.filter().order_by('-create_date')
        else:
            projects = Project.objects.order_by('-create_date')
        projects = projects.exclude(status__pk=2).exclude(status__pk=7)
        projectsfilter = ProjectFilterSet(projects, request.GET)
        context = {'projects': projectsfilter.qs, 'projectsfilter': projectsfilter, 'salesfilter': the_filter}
        return render(request, 'project_list.html', context)
    else:
        return render(request, 'not-authenticated.html')


def salesperson_list(request):
    if request.user.is_authenticated() and request.user.is_staff:
        sales_persons = SalesPerson.objects.all().order_by('user__last_name')
        context = {'sales_persons': sales_persons}
        return render(request, 'salesperson_list.html', context)
    else:
        return render(request, 'not-authenticated.html')


def salesperson_detail(request, user_id):
    if request.user.is_authenticated() and request.user.is_staff:
        sales_person = SalesPerson.objects.get(pk=user_id)
        projects = Project.objects.filter(sales_rep=sales_person).exclude(status__pk=2)
        context = {'sales_person': sales_person, 'projects': projects}
        return render(request, 'salesperson_detail.html', context)
    else:
        return render(request, 'not-authenticated.html')


def fundingadvisor_list(request):
    if request.user.is_authenticated() and request.user.is_staff:
        funding_advisors = FinanceAdvisor.objects.all().order_by('user__last_name')
        context = {'funding_advisors': funding_advisors}
        return render(request, 'fundingadvisor_list.html', context)
    else:
        return render(request, 'not-authenticated.html')


def fundingadvisor_detail(request, user_id):
    if request.user.is_authenticated() and request.user.is_staff:
        funding_advisor = FinanceAdvisor.objects.get(pk=user_id)
        projects = Project.objects.filter(funding_advisor=funding_advisor).exclude(status__pk=2)
        context = {'funding_advisor': funding_advisor, 'projects': projects}
        return render(request, 'fundingadvisor_detail.html', context)
    else:
        return render(request, 'not-authenticated.html')


def refunds(request):
    if request.user.is_authenticated() and request.user.is_staff:
        group = request.user.groups.values_list('name', flat=True)
        the_filter = request.user.username
        if group:
            if group[0] == "Sales Person":
                sales_filter = request.user.username
                projects = Project.objects.filter(sales_rep__user__username__startswith=sales_filter).order_by('-create_date')
            elif group[0] == "Funding Advisor":
                funding_filter = request.user.username
                projects = Project.objects.filter(funding_advisor__user__username__startswith=funding_filter).order_by('-create_date')
            else:
                projects = Project.objects.all().order_by('-create_date')
        else:
            projects = Project.objects.all().order_by('-create_date')
        projects = projects.filter(status__pk=2)
        projectsfilter = ProjectFilterSet(projects, request.GET)
        context = {'projects': projectsfilter.qs, 'projectsfilter': projectsfilter, 'salesfilter': the_filter}
        return render(request, 'project_list.html', context)
    else:
        return render(request, 'not-authenticated.html')


def process_refund(request, pk):
    project = Project.objects.get(pk=pk)
    status = Status.objects.get(title__iexact='refunded')
    project.refund_date = datetime.now()
    project.status = status
    project.save()
    return HttpResponseRedirect(reverse('drss.views.project_detail', args=(pk,)))


def assign_finance(request):
    if request.user.is_authenticated() and request.user.is_staff:
        group = request.user.groups.values_list('name', flat=True)
        the_filter = request.user.username
        if group:
            if group[0] == "Sales Person":
                sales_filter = request.user.username
                projects = Project.objects.filter(sales_rep__user__username__startswith=sales_filter).order_by('-create_date')
            elif group[0] == "Funding Advisor":
                funding_filter = request.user.username
                projects = Project.objects.filter(funding_advisor__user__username__startswith=funding_filter).order_by('-create_date')
            else:
                projects = Project.objects.all().order_by('-create_date')
        else:
            projects = Project.objects.all().order_by('-create_date')
        projects = projects.filter(funding_advisor=None)
        projectsfilter = ProjectFilterSet(projects, request.GET)
        context = {'projects': projectsfilter.qs, 'projectsfilter': projectsfilter, 'salesfilter': the_filter}
        return render(request, 'project_list.html', context)
    else:
        return render(request, 'not-authenticated.html')


def sales_deposit_log(request):
    if request.user.is_authenticated() and request.user.is_staff:
        payments = Payment.objects.all().order_by('-payment_date')
        paymentsfilter = PaymentFilterSet(payments, request.GET)
        context = {'payments': paymentsfilter.qs, 'paymentsfilter': paymentsfilter}
        return render(request, 'sales_deposit_log.html', context)
    else:
        return render(request, 'not-authenticated.html')


def project_detail(request, pk):
    if request.user.is_authenticated() and request.user.is_staff:
        project = Project.objects.get(pk=pk)
        documenttypes = DocumentType.objects.all()
        documents = project.document_set.all()
        sites = ShoppingCenter.objects.all()
        comments = project.comment_set.all().order_by('-post_date')
        payments = project.payment_set.all()
        tasks = Task.objects.all().filter(project=project).filter(project=project)
        incomplete_tasks = tasks.filter(completion=False).order_by('-scheduled_date')
        complete_tasks = tasks.filter(completion=True).order_by('-completion_date')
        context = {'project': project,
                   'documents': documents,
                   'comments': comments,
                   'payments': payments,
                   'documenttypes': documenttypes,
                   'incomplete_tasks': incomplete_tasks,
                   'complete_tasks': complete_tasks,
                   'sites': sites}
        return render(request, 'project_detail.html', context)
    else:
        return render(request, 'not-authenticated.html')


def site_detail(request, pk, site_id):
    if request.user.is_authenticated() and request.user.is_staff:
        site = ShoppingCenter.objects.get(pk=site_id)
        images = site.siteimage_set.all()
        context = {'site': site, 'images': images}
        return render(request, 'site_detail.html', context)
    else:
        return render(request, 'not-authenticated.html')


def site_create(request, pk):
    if request.method == 'POST':  # If the form has been submitted...
        form = CreateSite(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            form.save()
            return HttpResponseRedirect(reverse('drss.views.project_detail', args=(pk,)))  # Redirect after POST
    else:
        project = Project.objects.get(pk=pk)
        form = CreateSite(initial={project: pk})  # An unbound form

    return render(request, 'create_site.html', {
        'form': form,
    })


def project_create(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = SalesApplication(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            form.save()
            return HttpResponseRedirect('/projects')  # Redirect after POST
    else:
        form = SalesApplication()  # An unbound form

    return render(request, 'create.html', {
        'form': form,
    })


def deposit_detail(request, pk):
    group = request.user.groups.values_list('name', flat=True)
    if group:
        group = group[0]
    else:
        group = False
    if request.user.is_authenticated() and group == "Accounting":
        if request.method == 'POST':  # If the form has been submitted...
            form = NewDeposit(request.POST)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('drss.views.project_detail', args=(pk,)))  # Redirect after POST
        else:
            project = Project.objects.get(pk=pk)
            form = NewDeposit(initial={'project': project})  # An unbound form
        return render(request, 'deposit-detail.html', {
            'form': form,
        })
    else:
        return render(request, 'not_accounting.html')


def document_detail(request, pk):
    referrer = request.META["HTTP_REFERER"]
    if request.method == 'DELETE':
        Document.objects.get(pk=pk).delete()
        return HttpResponseRedirect(referrer)
    if request.method == 'POST':
        form = FileUpload(request.POST, request.FILES)
        if form.is_valid():
            doc = Document.objects.get(pk=pk)
            doc.document_file = request.FILES['docfile']
            doc.save()
            return HttpResponseRedirect(referrer)
    else:
        form = FileUpload()
     # Render upload box
    return HttpResponseRedirect(referrer)


#Real Estate Views
def loi_detail(request, pk):
    return render(request, 'loi_detail.html')

#API Views
class CommentList(generics.ListCreateAPIView):

    model = Comment
    serializer_class = CommentSerializer


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):

    model = Comment
    serializer_class = CommentSerializer


class DocumentList(generics.ListCreateAPIView):

    model = Document
    serializer_class = DocumentSerializer


class PaymentList(generics.ListCreateAPIView):

    model = Payment
    serializer_class = PaymentSerializer


class FinanceAdvisorList(generics.ListAPIView):

    queryset = User.objects.filter(groups__name='Funding Advisor')
    serializer_class = UserSerializer


class StatusList(generics.ListAPIView):

    model = Status
    serializer_class = StatusSerializer


class PaymentDetail(generics.RetrieveUpdateDestroyAPIView):

    model = Payment
    serializer_class = PaymentSerializer


class ProjectApi(generics.RetrieveUpdateDestroyAPIView):

    model = Project
    serializer_class = ProjectSerializer


@csrf_exempt
def payment_hook(request):
    json_data = simplejson.loads(request.raw_post_data)
    body = json_data['plain']
    msg = simplejson.loads(body)
    proj = Project.objects.get(last_name=msg['last_name'])
    payment = Payment(project=proj, payment_amount=msg['payment_amount'], last_four_num="xxxx", trace_number="xxxx", payment_type="Credit Card")
    payment.save()
    return HttpResponse('Payment Accepted')

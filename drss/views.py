from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from rest_framework import generics
from django.conf import settings
from drss.models import Project, Comment, Document, Payment, SalesPerson, FinanceAdvisor, Concept, DocumentType
from drss.forms import NewApplication, NewDeposit, FileUpload
from drss.serializers import CommentSerializer, DocumentSerializer, PaymentSerializer


def api_root(request):
    return HttpResponseRedirect('/projects')


def application(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = NewApplication(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            form.save()
            return HttpResponseRedirect('/thankyou')  # Redirect after POST
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
                form.save()
                return HttpResponseRedirect('/thankyou')  # Redirect after POST
        else:
            form = NewApplication(instance=app)  # Load Form for Verification
        if not app.signature:
            return render(request, 'application.html', {
                'form': form,
            })
        else:
            return render(request, 'completed-application.html')
    else:
        return render(request, 'not-authenticated.html')


def deposit(request, app_id):
    project = Project.objects.get(pk=app_id)
    if not project.is_paid():
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
    project = Project.objects.get(pk=app_id)
    documents = project.document_set.all()
    context = {'documents': documents}
    return render(request, 'documents.html', context)


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
    if request.user.is_authenticated():
        sales_filter = request.GET.get('sales', "")
        if sales_filter:
            projects = Project.objects.filter(sales_rep__user__username__startswith=sales_filter).order_by('last_name')
        else:
            projects = Project.objects.all().order_by('last_name')

        salespersons = SalesPerson.objects.all()
        fundingadvisors = FinanceAdvisor.objects.all()
        concepts = Concept.objects.all()
        context = {'projects': projects, 'salespersons': salespersons, 'fundingadvisors': fundingadvisors, 'concepts': concepts, 'salesfilter': sales_filter}
        return render(request, 'project_list.html', context)
    else:
        return render(request, 'not-authenticated.html')


def project_detail(request, pk):
    if request.user.is_authenticated():
        project = Project.objects.get(pk=pk)
        documenttypes = DocumentType.objects.all()
        documents = project.document_set.all()
        comments = project.comment_set.all().order_by('-post_date')
        payments = project.payment_set.all()
        context = {'project': project, 'documents': documents, 'comments': comments, 'payments': payments, 'documenttypes': documenttypes}
        return render(request, 'project_detail.html', context)
    else:
        return render(request, 'not-authenticated.html')


def deposit_detail(request, pk):
    if request.user.is_authenticated():
        if request.method == 'POST':  # If the form has been submitted...
            form = NewDeposit(request.POST)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('drss.views.list'))  # Redirect after POST
        else:
            form = NewDeposit()  # An unbound form
        return render(request, 'deposit-detail.html', {
            'form': form,
        })
    else:
        return render(request, 'not-authenticated.html')


def document_detail(request, pk):
      #Handle file upload
    if request.method == 'POST':
        form = FileUpload(request.POST, request.FILES)
        if form.is_valid():
            doc = Document.objects.get(pk=pk)
            doc.document_file = request.FILES['docfile']
            doc.save()
            referrer = request.META["HTTP_REFERER"]
            return HttpResponseRedirect(referrer)
    else:
        form = FileUpload()
     # Render upload box
    return HttpResponse(form.errors)


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


class PaymentDetail(generics.RetrieveUpdateDestroyAPIView):

    model = Payment
    serializer_class = PaymentSerializer

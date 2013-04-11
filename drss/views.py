from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from drss.models import Project, Comment, Document, Payment
from drss.forms import NewApplication
from drss.serializers import ProjectSerializer, CommentSerializer, DocumentSerializer, PaymentSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'projects': reverse('project-list', request=request),
        'comments': reverse('comment-list', request=request),
        'documents': reverse('document-list', request=request),
        'payments': reverse('payment-list', request=request),
    })


def application(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = NewApplication(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            form.save()
            return HttpResponseRedirect('/thankyou/')  # Redirect after POST
    else:
        form = NewApplication()  # An unbound form

    return render(request, 'application.html', {
        'form': form,
    })


def application_detail(request, app_id):
    if request.user.is_authenticated():
    # Do something for authenticated users.
        if request.method == 'POST':  # If the form has been submitted...
            app = Project.objects.get(pk=app_id)
            form = NewApplication(request.POST, instance=app)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                form.save()
                return HttpResponseRedirect('/thankyou/')  # Redirect after POST
        else:
            app = Project.objects.get(pk=app_id)
            form = NewApplication(instance=app)  # Load Form for Verification
        return render(request, 'application.html', {
            'form': form,
        })
    else:
        return render(request, 'not-authenticated.html')


def deposit(request, app_id):
    project = Project.objects.get(pk=app_id)
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
    context = {"secret_key": secret_key, "amount": amount,
               "last_name": last_name, "first_name": first_name, "address": address, "city": city, "state": state, "zip_code": zip_code,
               "home_phone": home_phone, "email": email,
               }
    return render(request, 'payment.html', context)


def thankyou(request):
    return render(request, 'thankyou.html')


class ProjectList(generics.ListCreateAPIView):

    model = Project
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):

    model = Project
    serializer_class = ProjectSerializer


class CommentList(generics.ListCreateAPIView):

    model = Comment
    serializer_class = CommentSerializer


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):

    model = Comment
    serializer_class = CommentSerializer


class DocumentList(generics.ListCreateAPIView):

    model = Document
    serializer_class = DocumentSerializer


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):

    model = Document
    serializer_class = DocumentSerializer


class PaymentList(generics.ListCreateAPIView):

    model = Payment
    serializer_class = PaymentSerializer


class PaymentDetail(generics.RetrieveUpdateDestroyAPIView):

    model = Payment
    serializer_class = PaymentSerializer
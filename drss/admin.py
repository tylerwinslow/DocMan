from django.contrib import admin
from django.core.urlresolvers import reverse
from django.conf import settings
from drss import models
from django.contrib.auth.models import User


class PaymentInline(admin.StackedInline):
    model = models.Payment
    extra = 1


class PackageInline(admin.StackedInline):
    model = models.PackageOption
    extra = 1


class UserInline(admin.StackedInline):
    model = models.User
    extra = 1


class CommentInline(admin.StackedInline):
    model = models.Comment
    extra = 1


class DocumentInline(admin.StackedInline):
    model = models.Document
    extra = 0


class SiteImageInline(admin.StackedInline):
    model = models.SiteImage
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    inlines = [PaymentInline, CommentInline, DocumentInline]
    list_display = ('last_name', 'first_name', 'concept', 'create_date', 'status', 'sales_rep', 'funding_advisor', 'deposit_amount', 'payment_info', 'state', 'store_size', 'advertising_source', 'refund_date')
    list_filter = ['sales_rep', 'funding_advisor']
    search_fields = ['last_name']
    date_hierarchy = 'create_date'


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'request_date', 'file_link')
    search_fields = ['project']

    def file_link(self, obj):
        if obj.document_file.name:
            path = obj.document_file.url
            return "<a href ='" + settings.BASE_URL + path + "'>Open File</a>"
        else:
            return "Not Yet Received"
    file_link.allow_tags = True


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('project', 'payment_date', 'payment_amount', 'payment_type', 'last_four_num', 'hold')


class ConceptAdmin(admin.ModelAdmin):
    inlines = [PackageInline]


class ShoppingCenterAdmin(admin.ModelAdmin):
    inlines = [SiteImageInline]


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Document, DocumentAdmin)
admin.site.register(models.DocumentType)
admin.site.register(models.Department)
admin.site.register(models.Status)
admin.site.register(models.ShoppingCenterStatus)
admin.site.register(models.Concept, ConceptAdmin)
admin.site.register(models.SiteLocator)
admin.site.register(models.CSM)
admin.site.register(models.LeasingManager)
admin.site.register(models.SalesPerson)
admin.site.register(models.FinanceAdvisor)
admin.site.register(models.AdvertisingSource)
admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.ShoppingCenter, ShoppingCenterAdmin)

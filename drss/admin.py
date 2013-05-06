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


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('email', 'status', 'refund_date'), ('first_name', 'last_name', 'social_security'), ('date_of_birth', 'address', 'city'), ('state', 'zip_code', 'best_call_time'),
                      ('home_phone', 'cell_phone', 'fax_number'))
        }),
        ('Partner', {
            'classes': ('collapse'),
            'fields': (('first_name_partner', 'last_name_partner', 'social_security_partner'),
                      ('date_of_birth_partner', 'address_partner', 'city_partner'), ('best_call_time_partner', 'state_partner', 'zip_code_partner'),
                      ('home_phone_partner', 'cell_phone_partner', 'fax_number_partner'))
        }),
        ('Store Information', {
            'classes': ('collapse'),
            'fields': (('concept', 'opening_location'), ('advertising_source', 'sales_rep', 'funding_advisor'), ('deposit_amount', 'store_size', 'package_price'))
        }),
        ('Finance Information', {
            'classes': ('collapse'),
            'fields': (('credit_score', 'place_of_employment', 'years_at_job', 'annual_salary'),
                      ('credit_score_partner', 'place_of_employment_partner', 'years_at_job_partner', 'annual_salary_partner'))
        }),
        ('Funding Assets Available', {
            'classes': ('collapse'),
            'fields': (('financing_cash', 'financing_loc', 'financing_hloc'), ('financing_401k', 'financing_pension', 'financing_ira'),
                      ('financing_stocksbonds', 'financing_cd', 'financing_lifeinsurance'))
        }),
        ('Liabilities', {
            'classes': ('collapse'),
            'fields': (('financing_credit', 'financing_financing_auto_loan', 'financing_mortgage_primary'), ('financing_mortgage_other', 'financing_installment', 'financing_debts_other'),)
        }),
    )
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


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Document, DocumentAdmin)
admin.site.register(models.DocumentType)
admin.site.register(models.Department)
admin.site.register(models.Status)
admin.site.register(models.Concept, ConceptAdmin)
admin.site.register(models.SalesPerson)
admin.site.register(models.FinanceAdvisor)
admin.site.register(models.AdvertisingSource)
admin.site.register(models.Payment, PaymentAdmin)

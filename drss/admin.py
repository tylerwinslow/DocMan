from django.contrib import admin
from django.conf import settings
from drss.models import Project, Concept, SalesPerson, FinanceAdvisor, Payment, Comment, Department, PackageOption, Document, DocumentType, AdvertisingSource
from django.contrib.auth.models import User


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 1


class PackageInline(admin.StackedInline):
    model = PackageOption
    extra = 1


class UserInline(admin.StackedInline):
    model = User
    extra = 1


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('email', ('first_name', 'last_name', 'social_security'), ('date_of_birth', 'address', 'city'), ('state', 'zip_code', 'best_call_time'),
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
    )
    inlines = [PaymentInline, CommentInline]
    list_display = ('last_name', 'create_date', 'sales_rep', 'funding_advisor', 'email', 'credit_score', 'is_paid', 'is_up_to_date')
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
    list_display = ('project', 'payment_amount', 'payment_type', 'last_four_num', 'hold')


class ConceptAdmin(admin.ModelAdmin):
    inlines = [PackageInline]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentType)
admin.site.register(Department)
admin.site.register(Concept, ConceptAdmin)
admin.site.register(SalesPerson)
admin.site.register(FinanceAdvisor)
admin.site.register(AdvertisingSource)
admin.site.register(Payment, PaymentAdmin)

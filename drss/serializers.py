from drss.models import Project, Comment, Document, Payment, FinanceAdvisor, Status
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    document_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    payment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        resource_name = 'project'
        fields = ('id', 'create_date', 'last_name', 'first_name', 'email', 'social_security', 'address', 'city', 'state', 'zip_code',
                  'store_size', 'concept', 'sales_rep', 'funding_advisor', 'date_of_birth', 'best_call_time', 'status',
                  'home_phone', 'cell_phone', 'fax_number', 'credit_score', 'place_of_employment', 'years_at_job', 'annual_salary',
                  'opening_location', 'deposit_amount', 'package_price', 'advertising_source',
                  'financing_cash', 'financing_loc', 'financing_hloc', 'financing_401k', 'financing_pension', 'financing_ira', 'financing_stocksbonds',
                  'financing_cd', 'financing_lifeinsurance', 'financing_credit', 'financing_financing_auto_loan', 'financing_mortgage_primary', 'financing_mortgage_other',
                  'financing_installment', 'financing_debts_other', 'comment_set', 'document_set', 'payment_set')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'project', 'author', 'post_date', 'internal', 'body')


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('id', 'project', 'title', 'request_date', 'document_file')


class FinanceAdvisorSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinanceAdvisor
        fields = ('id', 'full_name',)


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ('id', 'title')


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ('id', 'project', 'payment_amount', 'payment_type', 'trace_number', 'last_four_num', 'hold')

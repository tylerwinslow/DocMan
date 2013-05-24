from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from drss.models import Project
from templated_email import send_templated_mail


class Command(BaseCommand):
    help = 'Send Scheduled Communications'

    def handle(self, *args, **options):
        projects = Project.objects.all()
        number_emails = 0
        for project in projects:
            delta = project.create_date.replace(tzinfo=None) - datetime.now()
            if delta.days == -6 and project.funding_advisor:
                number_emails = number_emails + 1
                send_templated_mail(
                    template_name='financeday6',
                    from_email='notifications@drssmail.com',
                    recipient_list=[project.sales_rep.user.email, 'steve.castle@drssmail.com'],
                    context={
                        'project': project,
                    },
                )
        self.stdout.write('Sent "%s" emails' % number_emails)

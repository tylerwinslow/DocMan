from django.core.management.base import BaseCommand
from drss.models import Project


class Command(BaseCommand):
    help = 'Sets Assignment Date'

    def handle(self, *args, **options):
        projects = Project.objects.filter(assignment_date__isnull=True)
        for project in projects:
            payments = project.payment_set.all()
            if payments:
                project.assignment_date = payments[0].payment_date
                project.save()

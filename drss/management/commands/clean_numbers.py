from django.core.management.base import BaseCommand, CommandError
import re
from drss.models import Project


class Command(BaseCommand):
    help = 'Cleans Phone Numbers'

    def handle(self, *args, **options):
        projects = Project.objects.all()
        for project in projects:
            project.home_phone = re.sub("[^0-9]", "", project.home_phone)
            project.save()

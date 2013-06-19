import csv
from django.core.management.base import BaseCommand
from drss.models import Project


class Command(BaseCommand):
    help = 'Imports CSV File'

    def handle(self, *args, **options):
        with open("/home/ubuntu/docMan/imports/contact_tagger.csv", 'rb') as csvfile:
            data = csv.DictReader(csvfile)
            i = 0
            x = 0
            for item in data:
                try:
                    project = Project.objects.get(email__exact=item['email'])
                    project.act_id = item['act_id']
                    i = i + 1
                except:
                    project = Project(last_name=item['last_name'],
                                      first_name=item['first_name']
                                      )
                    project.save()
                    x = x + 1
        self.stdout.write("Number Found: " + str(i) + "Number Not Found: " + str(x))

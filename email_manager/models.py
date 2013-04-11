from django.db import models


class EmailType(models.Model):
    subject = models.CharField(max_length=100)
    body = models.TextField(max_length=100)

    def __unicode__(self):
        return self.subject


class EmailInstance(models.Model):
    email_type = models.ForeignKey(EmailType)
    send_date = models.DateTimeField('Send Date')
    email_from = models.EmailField('Email is From')
    email_to = models.EmailField('Email is To')

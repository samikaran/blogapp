import email
from unicodedata import name
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=300)
    # address= models.CharField(max_length=500)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    content = models.TextField(verbose_name=_('Message'))
    timeStamp = models.DateTimeField(verbose_name=_(
        "Sent at"), auto_now_add=True, blank=True)

    class Meta:
        ordering = ("-timeStamp",)
        verbose_name = _("Contact Form")
        verbose_name_plural = _("Contact Forms")

    def __str__(self):
        return 'Message from: ' + self.name + ' [' + self.email + ']'
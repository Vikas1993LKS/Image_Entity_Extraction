from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class StatusMixing(models.Model):
	is_active = models.BooleanField(_("active"), default=True, blank=False, null=False)
	is_deleted = models.BooleanField(_("deleted"), default=False, blank=False, null=False)

# Create your models here.
class Contact(TimeStampedModel, StatusMixing):
	person_name = models.CharField(_('Person Name'), max_length = 254, null = True, blank = True)
	contact_number = models.CharField(_('Contact Number'), max_length = 254, null = True, blank = True)
	email_id = models.CharField(_('Email Id'), max_length = 254, null = True, blank = True)
	organisation_name = models.TextField(_('Organisation Name'), null = True, blank = True)

	def __str__(self):
		return self.email_id


class CardModel(TimeStampedModel, StatusMixing):
	contact_details = models.ForeignKey("Contact", models.SET_NULL, blank = True, null = True)
	card_image = models.ImageField(_("Card Image"), blank = True, null = True)
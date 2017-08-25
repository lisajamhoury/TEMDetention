import logging

from twilio.rest import TwilioRestClient

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

logger = logging.getLogger(__name__)


class Followup(models.Model):
	name = models.CharField(max_length=50)
	body = models.TextField()

	def __unicode__(self):
		return self.name

class Fallback(models.Model):
	name = models.CharField(max_length=50)
	body = models.TextField()

	def __unicode__(self):
		return self.name

class TwilioNumber(models.Model):
	number = models.CharField(max_length=20)
	alpha_id = models.BooleanField(default=False)
	followup = models.ForeignKey(Followup, null=True)
	fallback = models.ForeignKey(Fallback, null=True)

	def __unicode__(self):
		return self.number 

	def get_caller_id(self):
		if self.alpha_id:
			return 'Dysturb'

		return self.number 


class Action(models.Model):
	twilio_number = models.ForeignKey(TwilioNumber)
	keyword = models.CharField(max_length=50) 
	audio_file = models.FileField(null=True, upload_to='audio', blank=True) 
	body = models.TextField(null=True, blank=True) 
	followup = models.TextField(null=True, blank=True)

	class Meta:
		unique_together = ('twilio_number', 'keyword')

	def __unicode__(self):
		return '%s / %s' % (self.twilio_number, self.keyword)

	def get_callback_url(self):
		return settings.BASE_URL + reverse('followup')


	def perform(self, user_number):
		if self.audio_file: 
			call = client.calls.create(
				to=user_number.number, 
				from_=self.twilio_number.number, 
				method='GET',
				url=self.audio_file.url,
				status_callback=self.get_callback_url()
			) 
			
			outbound = Outbound(
				from_number=self.twilio_number,
				to_number=user_number,
				action=self,
				twilio_sid=call.sid 
			)
			
			outbound.save()

		if not self.audio_file:
			message = client.messages.create(
				body=self.body,
				to=user_number.number,
				from_=self.twilio_number.number
			)



class User(models.Model):
	number = models.CharField(max_length=20)
	subscribed = models.BooleanField(default=False)

	def __unicode__(self):
		return self.number

	def subscribe(self, twilio_number):
		thanks = "Thanks for subscribing. You'll hear from us soon."
		self.subscribed = True

		message = client.messages.create(
			body=thanks,
			to=self.number,
			from_=twilio_number.number
			)

		self.save()


class Inbound(models.Model):
	from_number = models.ForeignKey(User)
	to_number = models.ForeignKey(TwilioNumber)
	body = models.CharField(max_length=140)
	action = models.ForeignKey(Action, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	twilio_sid = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return 'inbound on %s from %s: %s (%s)' % (self.created_formatted, self.from_number, self.body, self.twilio_sid)

	@property 
	def created_formatted(self):
		return self.created.strftime('%m/%d/%Y')		

	@classmethod
	def create_from_twilio_request(cls, twilio_request):
		pass

class Outbound(models.Model):
	from_number = models.ForeignKey(TwilioNumber)
	to_number = models.ForeignKey(User)
	action = models.ForeignKey(Action)
	created = models.DateTimeField(auto_now_add=True)
	twilio_sid = models.CharField(max_length=200, blank=True)
	followup_sent = models.BooleanField(default=False)	

	def __unicode__(self):
		return 'outbound to %s: %s' % (self.to_number, self.twilio_sid)

	def send_followup(self): 

		followup = None

		if self.from_number.followup:
			followup = self.from_number.followup.body
	
		if self.action.followup:
			followup = self.action.followup

		if not self.followup_sent and followup is not None:	
			message = client.messages.create(
				body=followup,
				to=self.to_number.number,
				from_=self.from_number.get_caller_id()
			)

			self.followup_sent = True
			self.save()




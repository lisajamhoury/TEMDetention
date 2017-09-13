import logging

from twilio.rest import Client

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

logger = logging.getLogger(__name__)


class Followup(models.Model):
	name = models.CharField(max_length=50, help_text='Used for identification within admin')
	body = models.TextField(help_text='Text message to be sent to user')

	def __str__(self):
		return self.name

class Fallback(models.Model):
	name = models.CharField(max_length=50, help_text='Used for identification within admin')
	body = models.TextField(help_text='Text message to be sent to user')

	def __str__(self):
		return self.name

class Reprompt(models.Model):
	name = models.CharField(max_length=50, help_text='Used for identification within admin')
	body = models.TextField(help_text='Text message to be sent to user')

	def __str__(self):
		return self.name 

class TwilioNumber(models.Model):
	number = models.CharField(max_length=20, help_text='Create number in Twilio before entering here. Include plus sign and country code. ie +1')
	alpha_id = models.BooleanField(default=False)
	followup = models.ForeignKey(Followup, null=True, help_text='Default followup for this phone number')
	fallback = models.ForeignKey(Fallback, null=True, help_text='Default fallback for this phone number')
	reprompt = models.ForeignKey(Reprompt, null=True, help_text='Default reprompt for this phone number')

	def __str__(self):
		return self.number 

	def get_caller_id(self):
		if self.alpha_id:
			return 'Newest Americans'

		return self.number 


class Action(models.Model):
	twilio_number = models.ForeignKey(TwilioNumber)
	keyword = models.CharField(max_length=50, help_text='Word for user text in. Must be all lowercase.') 
	audio_file = models.FileField(null=True, upload_to='audio', blank=True) 
	body = models.TextField(null=True, blank=True, help_text='Overrides audio. Only add if no audio') 
	followup = models.TextField(null=True, blank=True, help_text='Overrides default followup for phone number')
	reprompt = models.TextField(null=True, blank=True, help_text='Overrides default reprompt for phone number')

	class Meta:
		unique_together = ('twilio_number', 'keyword')

	def __str__(self):
		return '%s / %s' % (self.twilio_number, self.keyword)

	def get_callback_url(self):
		return settings.BASE_URL + reverse('followup')

	def get_answeredby_url(self):
		return settings.BASE_URL + reverse('answeredby')


	def perform(self, user_number):
		if self.audio_file: 
			call = client.calls.create(
				to=user_number.number, 
				from_=self.twilio_number.number, 
				method='GET',
				url=self.get_answeredby_url(),
				machine_detection='Enable',
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

	def __str__(self):
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

	def __str__(self):
		return 'inbound on %s from %s: %s (%s)' % (self.created_formatted, self.from_number, self.body, self.twilio_sid)

	@property 
	def created_formatted(self):
		return self.created.strftime('%m/%d/%Y')		

	@classmethod
	def create_from_twilio_request(cls, twilio_request, twilio_number, user):
		inbound = cls()
		inbound.from_number = user
		inbound.to_number = twilio_number
		inbound.body = twilio_request.body.lower()
		inbound.twilio_sid = twilio_request.smssid
		inbound.save()
		
		return inbound


class Outbound(models.Model):
	from_number = models.ForeignKey(TwilioNumber)
	to_number = models.ForeignKey(User)
	action = models.ForeignKey(Action)
	created = models.DateTimeField(auto_now_add=True)
	duration = models.CharField(max_length=100, blank=True)
	twilio_sid = models.CharField(max_length=200, blank=True)
	followup_sent = models.BooleanField(default=False)	
	reprompt_sent = models.BooleanField(default=False)
	answered_by = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return 'outbound to %s: %s' % (self.to_number, self.twilio_sid)

	def send_reprompt(self):

		reprompt = None

		if self.from_number.reprompt:
			reprompt = self.from_number.reprompt.body

		if self.action.reprompt:
			reprompt = self.action.reprompt

		if not self.reprompt_sent and reprompt:
			message = client.messages.create(
				body=reprompt,
				to=self.to_number.number,
				from_=self.from_number.get_caller_id()
			)

			self.reprompt_sent = True 
			self.save()


	def send_followup(self): 

		followup = None

		if self.from_number.followup:
			followup = self.from_number.followup.body
	
		if self.action.followup:
			followup = self.action.followup

		if not self.followup_sent and followup:	
			message = client.messages.create(
				body=followup,
				to=self.to_number.number,
				from_=self.from_number.get_caller_id()
			)

			self.followup_sent = True
			self.save()


	@classmethod
	def find_most_recent_call(cls, user):
		outbound = cls.objects\
			.filter(to_number=user)\
			.order_by('-created')\
			.exclude(answered_by__in=['human', 'unknown']).first()

		return outbound


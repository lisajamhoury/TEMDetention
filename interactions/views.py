import logging

from django_twilio.decorators import twilio_view
from django_twilio.request import decompose
from twilio.rest import Client
from twilio.twiml.voice_response import Play, VoiceResponse

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden

from interactions.models import Inbound, Outbound, TwilioNumber, User, Action
from twilio.request_validator import RequestValidator

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

logger = logging.getLogger(__name__)

@twilio_view
def sms(request):
	twilio_request = decompose(request)

	user, created = User.objects.get_or_create(number=twilio_request.from_)
	twilio_number, created = TwilioNumber.objects.get_or_create(number=twilio_request.to)
	
	inbound = Inbound.create_from_twilio_request(twilio_request, twilio_number, user)

	body = twilio_request.body.lower()

	if body == 'subscribe':
		user.subscribe(twilio_number)
		
		return HttpResponse()

	if body == 'yes':
		outbound = Outbound.find_most_recent_call(user)

		action = outbound.action 
		action.perform(user)
		
		inbound.action = action
		inbound.save()

		return HttpResponse()

	try:
		action = Action.objects.get(keyword=inbound.body, twilio_number=twilio_number)
		action.perform(user)

		inbound.action = action
		inbound.save()

	except Action.DoesNotExist:
		message = client.messages.create(
				body=twilio_number.fallback.body,
				to=user.number,
				from_=twilio_number.number 
			)
	
	return HttpResponse()

@twilio_view
def followup(request):
	twilio_request = decompose(request)

	outbound = Outbound.objects.get(twilio_sid=twilio_request.callsid)

	outbound.duration = twilio_request.callduration
	outbound.save()

	if outbound.answered_by in ['human', 'unknown']:
		outbound.send_followup()

	else: 
		outbound.send_reprompt()

	return HttpResponse()

def answeredby(request):
	# build validator manually because decorator not working
	logger.info(request.build_absolute_uri())
	twilio_request = decompose(request)
	validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

	# Validate the request using its URL, POST data,
	# and X-TWILIO-SIGNATURE header
	request_valid = validator.validate(
		request.build_absolute_uri(),
		request.POST,
		request.META.get('HTTP_X_TWILIO_SIGNATURE', ''))
	
	if not request_valid:
		return HttpResponseForbidden()

	outbound = Outbound.objects.get(twilio_sid=twilio_request.callsid)
	response = VoiceResponse()

	if twilio_request.answeredby in ['human', 'unknown']:
		response.play(outbound.action.audio_file.url)

	else: 
		response.hangup()

	outbound.answered_by = twilio_request.answeredby
	outbound.save()

	return HttpResponse(response) 














from import_export import resources, fields
from import_export.admin import ExportMixin

from django.contrib import admin

from interactions.models import Fallback
from interactions.models import Followup
from interactions.models import TwilioNumber
from interactions.models import Action
from interactions.models import User
from interactions.models import Inbound
from interactions.models import Outbound

class InboundResource(resources.ModelResource):
	created_formatted = fields.Field(attribute='created_formatted')

	class Meta:
		model = Inbound
		fields = ('from_number__number', 'to_number__number', 'action__keyword', 'body', 'created_formatted')


class InboundAdmin(ExportMixin, admin.ModelAdmin):
	list_filter = ('from_number', 'to_number__number', 'action', 'body')
	list_display = ('from_number', 'to_number', 'action', 'body', 'created_formatted')
	resource_class = InboundResource
	

admin.site.register(Fallback)
admin.site.register(Followup)
admin.site.register(TwilioNumber)
admin.site.register(Action)
admin.site.register(User)
admin.site.register(Inbound, InboundAdmin)
admin.site.register(Outbound)




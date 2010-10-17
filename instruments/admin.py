from django.contrib import admin
from instruments.models import Instrument

class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('number', 'name')
    ordering = ('number',)

admin.site.register(Instrument, InstrumentAdmin)

from django.contrib import admin
from .models import Simulator

@admin.register(Simulator)
class SimulatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'interval', 'kpi_id')
    list_filter = ('start_date', 'interval')
    search_fields = ('id', 'kpi_id__formula')
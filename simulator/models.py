from django.db import models

class Simulator(models.Model):
    start_date = models.DateTimeField()
    interval = models.IntegerField(help_text="Interval in seconds")
    kpi_id = models.ForeignKey('kpis.KPI', on_delete=models.CASCADE)

    def __str__(self):
        return f"Simulator {self.id} - KPI: {self.kpi_id}"

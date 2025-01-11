from django.db import models

class KPI(models.Model):
    formula = models.CharField(max_length=255)

    def apply_formula(self, value):
        return eval(self.formula.replace('x', str(value)))

    def __str__(self):
        return f"KPI {self.id}: {self.formula}"
from django.db import models


class Verbe(models.Model):
    present = models.fields.CharField(max_length=50, blank=True)
    preterit = models.fields.CharField(max_length=50, blank=True)
    participe_passe = models.fields.CharField(max_length=50, blank=True)
    francais = models.fields.CharField(max_length=50)

    def __str__(self):
        return f'{self.francais}'


class Table(models.Model):
    class Meta:
        db_table = ''
    verbe = models.fields.ForeignKey(Verbe, on_delete=medels.SET_NULL)

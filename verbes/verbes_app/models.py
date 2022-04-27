from django.db import models

class Verbes(models.Model):
    present = models.fields.CharField(max_length=50, blank=True)
    preterit = models.fields.CharField(max_length=50, blank=True)
    participe_passe = models.fields.CharField(max_length=50, blank=True)
    francais = models.fields.CharField(max_length=50)

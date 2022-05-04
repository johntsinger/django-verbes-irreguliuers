from django.db import models


class Verbe(models.Model):
    present = models.fields.CharField(max_length=50, blank=True)
    preterit = models.fields.CharField(max_length=50, blank=True)
    participe_passe = models.fields.CharField(max_length=50, blank=True)
    francais = models.fields.CharField(max_length=50)
    done = models.fields.BooleanField(default=False)
    success = models.fields.BooleanField(default=False)

    def __str__(self):
        return f'{self.present} {self.preterit} {self.participe_passe} \
{self.francais}'


class Table(models.Model):
    name = models.fields.CharField(max_length=30)
    verbes = models.ManyToManyField(Verbe)

    def __str__(self):
        return f'{self.name}'
      
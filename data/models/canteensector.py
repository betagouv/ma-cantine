from django.db import models
from .canteen import Canteen
from .sector import Sector


class CanteenSectorRelation(models.Model):
    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)

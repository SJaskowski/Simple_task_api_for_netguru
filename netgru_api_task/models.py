from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Car(models.Model):
    class Meta:
        unique_together = ('make_name', 'model_name',)

    make_name = models.CharField(max_length=200, null=True, blank=True)
    model_name = models.CharField(max_length=200, null=True, blank=True)


class Rating(models.Model):
    car = models.ForeignKey(Car, related_name="ratings", on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(0),
                                            MaxValueValidator(5)])

    def __str__(self):
        return str(self.score)

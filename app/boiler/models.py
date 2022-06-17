from calendar import day_abbr
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

days = ["Hoy","lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
yesno = ["no","si"]


class Programs(models.Model):
    # 1 = lunes 7 = domingo, 0 = hoy
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    minutes = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)])
    duration = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)])
    active = models.BooleanField(default=True)
    unic = models.BooleanField(default=False)
    startTime = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24*60)],default=0)
    endTime = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(48*60)],default=0)

    class Meta:
        ordering = ("day","hour","minutes")

    def save(self,*args, **kwargs):
        self.startTime = self.hour*60+self.minutes
        self.endTime = self.startTime + int(self.duration)
        super().save(*args,**kwargs)

    def __str__(self):
        active = yesno[self.active]
        unic = yesno[self.unic]
        return f"{days[self.day]} a las {self.hour:02}:{self.minutes:02} por {self.duration:02} mins. (activo: {active}, único: {unic}) "


class CurrentProgram(models.Model):
    # 1 = lunes 7 = domingo, 0 = hoy
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    minutes = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)])
    duration = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(24*60)])
    startTime = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24*60)],default=0)
    endTime = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(48*60)],default=0)

    def save(self,*args, **kwargs):
        self.startTime = self.hour*60+self.minutes
        self.endTime = self.startTime + int(self.duration)
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{days[self.day]} a las {self.hour:02}:{self.minutes:02} por {self.duration:02} mins. "




# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import json
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F


class Station(models.Model):
    station_code = models.CharField(primary_key=True, max_length=10, blank=False)
    name_chinese = models.CharField(max_length=20, blank=True, null=True)
    name_english = models.CharField(max_length=50, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=False)
    lon = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=False)
    elev = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=False)
    gain = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=False)

    def __str__(self):
        return self.station_code

    class Meta:
        managed = False
        db_table = 'TTSN_Station'


class Data(models.Model):
    file_name = models.CharField(primary_key=True, max_length=50, blank=False)
    station = models.CharField(max_length=10, blank=True, null=True)
    component = models.CharField(max_length=3, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.file_name

    class Meta:
        managed = False
        db_table = 'TTSN_Data'

############### admin ################


# class CustomUser(AbstractUser):
#     email = models.EmailField(blank=False, max_length=254, verbose_name="email address")
#     is_approved = models.BooleanField(default=False)

#     USERNAME_FIELD = "username"
#     EMAIL_FIELD = "email"         # e.g: "email", "primary_email"

#     # class Meta:
#     #     # managed = False
#     #     # db_table = 'backend_customuser'
#     #     verbose_name_plural = 'User'  # 後臺的顯示名稱

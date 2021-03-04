import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings

# Verificar relação ForeignKey Address


class MicrogridAddress(models.Model):
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    street_and_number = models.CharField(max_length=100)

    # class Meta:
    #     unique_together = ['city', 'country', 'zip_code', 'state', 'street_and_number']


class Microgrid(models.Model):
    microgrid_id = models.IntegerField(unique=True)
    microgrid_key = models.CharField(max_length=50)
    microgrid_name = models.CharField(max_length=50)
    client_name = models.CharField(max_length=50)
    client_id = models.IntegerField()
    time_zone = models.CharField(max_length=50)
    address = models.ForeignKey(MicrogridAddress, on_delete = models.CASCADE)


class MicrogridParameters(models.Model):
    microgrid = models.OneToOneField(Microgrid, on_delete = models.CASCADE)
    connection_type = models.CharField(max_length=50)
    diesel_price = models.FloatField()
    natural_gas_price = models.FloatField()
    utility_name = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    subgroup = models.CharField(max_length=50)
    tariff_type = models.CharField(max_length=50)
    pis_cofins = models.FloatField()
    icms_1_value = models.FloatField()
    icms_1_limit = models.FloatField()
    icms_2_value = models.FloatField()
    icms_2_limit = models.FloatField()
    icms_3_value = models.FloatField()
    icms_3_limit = models.FloatField()
    tusd_d_peak = models.FloatField()
    tusd_e_peak = models.FloatField()
    tusd_e_intermediary = models.FloatField()
    tusd_d_base = models.FloatField()
    tusd_e_base = models.FloatField()
    energy_price_peak = models.FloatField()
    energy_price_intermediary = models.FloatField()
    energy_price_base = models.FloatField()
    tariff_flag_signal = models.CharField(max_length=50)


class MicrogridComponent(models.Model):
    microgrid = models.ForeignKey(Microgrid, on_delete = models.CASCADE)
    component_id = models.IntegerField()
    operation_status = models.CharField(max_length=50)
    component_type = models.CharField(max_length=50)
    meters_id = models.IntegerField()

class StaticConfig(models.Model):
    component = models.ForeignKey(MicrogridComponent, on_delete = models.CASCADE)
    key = models.CharField(max_length=50)
    value = models.FloatField()

class DataPoints(models.Model):
    data_id = models.IntegerField()
    component = models.ForeignKey(MicrogridComponent, on_delete = models.CASCADE)
    key = models.CharField(max_length=50)
    data_type = models.CharField(max_length=50)

class Measurements(models.Model):
    data_id = models.ForeignKey(DataPoints, on_delete = models.CASCADE)
    minimum = models.FloatField()
    maximum = models.FloatField()
    average = models.FloatField()
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    timestamps = models.DateTimeField()

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from datetime import datetime, timedelta
from django.core.validators import RegexValidator

from shared.models import BaseModel

ORDINARY_USER, MANAGER, SUPER_ADMIN = (
    "ordinary_user",
    "manager",
    "super_admin"
)

VIA_USERNAME, VIA_EMAIL, VIA_PHONE = (
    "via_username", 
    "via_email",
    "vie_phone"
)

MALE, FEMALE = (
    "male",
    "female"
)

PHONE_EXPIRE = 3
EMAIL_EXPIRE = 5


class UserConfirmation(models.Model):
    TYPE_CHOISE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )
    
    code = models.CharField(max_length=4)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    verify_type = models.CharField(max_length=20, choices=TYPE_CHOISE)
    expration_date = models.DateTimeField(null=True)
    is_comfirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user.__str__())
    
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.verify_type == VIA_EMAIL:
                self.expration_date = datetime.now() + timedelta(minutes=EMAIL_EXPIRE)
            else:
                self.expration_date = datetime.now() + timedelta(minutes=PHONE_EXPIRE)

        super(UserConfirmation, self).save(*args, **kwargs)
        

class User(AbstractUser, BaseModel):
    _validate_phone = RegexValidator(
        regex="(0|91)?[7-9][0-9]{9}",
        message="Telefon raqam Xalqaro Formatda 998YYXXXXXXX ko'rinishida kiritilishi kerak!"
    )
    USER_ROLES = (
        (ORDINARY_USER, ORDINARY_USER),
        (MANAGER, MANAGER),
        (SUPER_ADMIN, SUPER_ADMIN)
    )
    
    AUTH_TYPE = (
        (VIA_USERNAME, VIA_USERNAME),
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )
    
    GENDER_TYPE = (
        (MALE, MALE),
        (FEMALE, FEMALE)
    )
    
    
    user_role = models.CharField(max_length=20, choices=USER_ROLES, default=ORDINARY_USER)
    auth_type = models.CharField(max_length=20, choices=AUTH_TYPE, default=VIA_USERNAME)
    email = models.EmailField(null=True, unique=True)
    phone = models.CharField(max_length=15, null=True, unique=True, validators=[_validate_phone])
    bio = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def create_verify_code(self, verify_type):
        code = "".join([str(random.randint(0,100) % 10)for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id,
            verify_type=verify_type,
            code=code
        )
        return code
        
        
import uuid

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class User(AbstractUser, BaseModel):
	class Meta:
		verbose_name = _("Account")
		verbose_name_plural = _("Accounts")

	class Role(models.TextChoices):
		ADMINISTRATOR = "AD", _("Administrator")
		STUDENT = "STU", _("Sinh viên")
		MANAGER = "MAG", _("Quản lý")
		SPECIALIST = "SPC", _("Chuyên viên cộng tác sinh viên")

	class Gender(models.TextChoices):
		MALE = "M", _("Nam")
		FEMALE = "F", _("Nữ")
		UNKNOWN = "U", _("Khác")

	email = models.EmailField(null=False, blank=False, unique=True)
	avatar = CloudinaryField(null=True, blank=True)
	full_name = models.CharField(max_length=255, null=False, blank=False)
	dob = models.DateField(null=False, blank=False)
	gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.UNKNOWN)
	address = models.CharField(max_length=255, null=True, blank=True)
	phone = models.CharField(max_length=15, null=True, blank=True, unique=True)
	identification = models.CharField(max_length=36, null=False, blank=False, unique=True)
	role = models.CharField(max_length=10, null=True, blank=True, choices=Role.choices, default=Role.STUDENT)
	code = models.UUIDField(null=False, blank=False, unique=True, db_index=True, editable=False, default=uuid.uuid4)

	username = None
	first_name = None
	last_name = None

	from users.managers import UserManager
	objects = UserManager()

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.email

	@property
	def original_role(self):
		return self.Role.labels[self.Role.values.index(self.role)]

	@property
	def original_gender(self):
		return self.Gender.labels[self.Role.values.index(self.gender)]

	@staticmethod
	def get_role_from_string(role_str):
		role_str_lower = role_str.lower()
		try:
			index = User.Role.labels.index(role_str_lower)
			return User.Role.values[index]
		except ValueError:
			return None


class Administrator(BaseModel):
	class Meta:
		verbose_name = _("Administrator")
		verbose_name_plural = _("Administrators")

	user = models.OneToOneField(to=User, null=False, blank=False, on_delete=models.CASCADE, related_name="%(class)s", )


class Manager(BaseModel):
	class Meta:
		verbose_name = _("Assistant")
		verbose_name_plural = _("Assistants")

	certificate = models.CharField(max_length=50, null=False, blank=False)
	user = models.OneToOneField(to=User, null=False, blank=False, on_delete=models.CASCADE, related_name="%(class)s", )


class Specialist(BaseModel):
	class Meta:
		verbose_name = _("Specialist")
		verbose_name_plural = _("Specialists")

	degree = models.CharField(max_length=50, null=False, blank=False)
	user = models.OneToOneField(to=User, null=False, blank=False, on_delete=models.CASCADE, related_name="%(class)s", )


class Student(BaseModel):
	class Meta:
		verbose_name = _("Student")
		verbose_name_plural = _("Students")

	university = models.CharField(max_length=50, null=False, blank=False)
	major = models.CharField(max_length=50, null=False, blank=False)
	user = models.OneToOneField(to=User, null=False, blank=False, on_delete=models.CASCADE, related_name="%(class)s", )

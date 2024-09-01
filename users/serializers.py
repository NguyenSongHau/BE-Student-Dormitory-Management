import re

from rest_framework import serializers

from base.serializers import BaseSerializer
from users.models import User, Administrator, Manager, Specialist, Student
from utils import validations


class UserSerializer(BaseSerializer):
	# Cho Manager
	certificate = serializers.CharField(max_length=50, write_only=True, required=False)
	# Cho Specialist
	degree = serializers.CharField(max_length=50, write_only=True, required=False)
	# Cho Student
	university = serializers.CharField(max_length=50, write_only=True, required=False)
	major = serializers.CharField(max_length=50, write_only=True, required=False)

	user_instance = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = User
		fields = [
			"id", "role", "email", "password", "identification", "full_name", "avatar",
			"dob", "gender", "address", "phone", "code", "date_joined", "last_login", "user_instance",
			"certificate", "degree", "university", "major",
		]
		extra_kwargs = {
			"gender": {"read_only": True},
			"address": {"read_only": True},
			"phone": {"read_only": True},
			"code": {"read_only": True},
			"date_joined": {"read_only": True},
			"last_login": {"read_only": True},
			"password": {"write_only": True},
		}

	def to_representation(self, account):
		data = super().to_representation(account)
		avatar = data.get("avatar")

		if "avatar" in self.fields and avatar:
			data["avatar"] = account.avatar.url

		return data

	def create(self, validated_data):
		other_field = {
			"certificate": validated_data.pop("certificate", None),
			"degree": validated_data.pop("degree", None),
			"university": validated_data.pop("university", None),
			"major": validated_data.pop("major", None),
		}

		user = User.objects.create_user(email=validated_data.pop("email"), password=validated_data.pop("password"), **validated_data)
		self.create_user_instance(user, **other_field)

		return user

	def get_user_instance(self, user):
		serializer_class, instance_name = validations.check_user_role(user)
		user_instance = getattr(user, instance_name, None)

		return serializer_class(user_instance).data

	def validate_role(self, role):
		if role is None or role not in User.Role.values:
			raise serializers.ValidationError({"message": "Vai trò không hợp lệ."})

		if role == User.Role.ADMINISTRATOR:
			raise serializers.ValidationError({"message": "Không thể tạo tài khoản quản trị viên."})

		return role

	def validate_email(self, email):
		if email is None or not re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email.strip()):
			raise serializers.ValidationError({"message": "Email không đúng định dạng."})

		return email

	def validate_password(self, password):
		if password is None or not re.fullmatch(r"^.{6,}$", password.strip()):
			raise serializers.ValidationError({"message": "Mật khẩu phải chứa ít nhất 6 ký tự."})

		return password

	def validate_identification(self, identification):
		if identification is None or not re.fullmatch(r"^[0-9]{9,12}$", identification.strip()):
			raise serializers.ValidationError({"message": "Số CCCD không hợp lệ."})

		return identification

	def create_user_instance(self, user, **other_field):
		if user.role == User.Role.MANAGER:
			certificate = other_field.get("certificate", None)

			if not certificate:
				raise serializers.ValidationError({"message": "Vui lòng nhập chứng chỉ."})

			Manager.objects.create(user=user, certificate=certificate)
		elif user.role == User.Role.SPECIALIST:
			degree = other_field.get("degree", None)

			if not degree:
				raise serializers.ValidationError({"message": "Vui lòng nhập bằng cấp."})

			Specialist.objects.create(user=user, degree=degree)
		elif user.role == User.Role.STUDENT:
			university = other_field.get("university", None)
			major = other_field.get("major", None)

			if not university or not major:
				raise serializers.ValidationError({"message": "Vui lòng nhập trường và ngành học."})

			Student.objects.create(user=user, university=university, major=major)


class UserUpdateSerializer(serializers.Serializer):
	old_password = serializers.CharField(write_only=True, required=False)
	new_password = serializers.CharField(write_only=True, required=False)
	email = serializers.EmailField(required=False)
	avatar = serializers.ImageField(required=False)
	full_name = serializers.CharField(max_length=255, required=False)
	dob = serializers.DateField(required=False)
	gender = serializers.CharField(max_length=1, required=False)
	address = serializers.CharField(max_length=255, required=False)
	phone = serializers.CharField(max_length=15, required=False)
	# Cho Manager
	certificate = serializers.CharField(max_length=50, required=False)
	# Cho Specialist
	degree = serializers.CharField(max_length=50, required=False)
	# Cho Student
	university = serializers.CharField(max_length=50, required=False)
	major = serializers.CharField(max_length=50, required=False)

	def update(self, user, validated_data):
		other_field = {
			"certificate": validated_data.pop("certificate", None),
			"degree": validated_data.pop("degree", None),
			"university": validated_data.pop("university", None),
			"major": validated_data.pop("major", None),
		}

		if "old_password" in validated_data and "new_password" in validated_data:
			user.set_password(validated_data.pop("new_password"))
		if "avatar" in validated_data:
			user.avatar = validated_data.pop("avatar")
		for attr, value in validated_data.items():
			setattr(user, attr, value)
		user.save()

		self.update_user_instance(user, **other_field)

		return user

	def validate_email(self, email):
		if not re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email.strip()):
			raise serializers.ValidationError({"message": "Email không đúng định dạng."})

		return email

	def validate_new_password(self, new_password):
		if not re.fullmatch(r"^.{6,}$", new_password.strip()):
			raise serializers.ValidationError({"message": "Mật khẩu phải chứa ít nhất 6 ký tự."})

		return new_password

	def validate_identification(self, identification):
		if not re.fullmatch(r"^[0-9]{9,12}$", identification.strip()):
			raise serializers.ValidationError({"message": "Số CCCD không hợp lệ."})

		return identification

	def update_user_instance(self, user, **other_field):
		instance_name = validations.check_user_role(user)[1]
		user_instance = getattr(user, instance_name, None)

		if user.role == User.Role.MANAGER:
			certificate = other_field.get("certificate", None)

			user_instance.certificate = certificate if certificate else user_instance.certificate
		elif user.role == User.Role.SPECIALIST:
			degree = other_field.get("degree", None)

			user_instance.degree = degree if degree else user_instance.degree
		elif user.role == User.Role.STUDENT:
			university = other_field.get("university", None)
			major = other_field.get("major", None)

			user_instance.university = university if university else user_instance.university
			user_instance.major = major if major else user_instance.major

		user_instance.save()


class BaseInstanceSerializer(BaseSerializer):
	class Meta:
		exclude = ["user", "is_active", "created_date", "updated_date"]


class AdministratorSerializer(BaseSerializer):
	class Meta:
		model = Administrator
		exclude = BaseInstanceSerializer.Meta.exclude


class ManagerSerializer(BaseSerializer):
	class Meta:
		model = Manager
		exclude = BaseInstanceSerializer.Meta.exclude


class SpecialistSerializer(BaseSerializer):
	class Meta:
		model = Specialist
		exclude = BaseInstanceSerializer.Meta.exclude


class StudentSerializer(BaseSerializer):
	class Meta:
		model = Student
		exclude = BaseInstanceSerializer.Meta.exclude

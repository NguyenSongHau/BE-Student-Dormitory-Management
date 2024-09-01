from rest_framework.exceptions import ValidationError

from utils import validations


def set_role_for_account(user, account):
	role = validations.check_user_instance(user)[1]

	if not role:
		raise ValidationError({"detail": "Người dùng không hợp lệ"})

	account.role = role
	account.save()

	return user, account


def get_all_subclasses(cls):
	all_subclasses = []

	for subclass in cls.__subclasses__():
		if not subclass._meta.abstract:
			all_subclasses.append(subclass)
		all_subclasses.extend(get_all_subclasses(subclass))

	return all_subclasses

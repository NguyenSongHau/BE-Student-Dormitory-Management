from rest_framework import permissions


class OwnerComment(permissions.IsAuthenticated):
	def has_object_permission(self, request, view, comment):
		return super().has_permission(request, view) and request.user_instance == comment.account

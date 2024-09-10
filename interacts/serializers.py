from rest_framework import serializers

from base.serializers import BaseSerializer
from interacts.models import Comment
from users import serializers as users_serializer


class CommentSerializer(BaseSerializer):
	user = serializers.SerializerMethodField()
	post = serializers.SerializerMethodField()

	class Meta:
		model = Comment
		fields = ["id", "created_date", "updated_date", "content", "user", "post"]

	def get_account(self, comment):
		serializer = users_serializer.UserSerializer(comment.user)

		return serializer.data

	def get_room(self, comment):
		serializer = users_serializer.PostSerializer(comment.post)

		return serializer.data

from rest_framework import serializers

from base.serializers import BaseSerializer
from rental.models import Room, Bed, Post


class RoomSerializer(BaseSerializer):
	beds = serializers.SerializerMethodField()

	class Meta:
		model = Room
		fields = ["id", "name", "image", "number_of_bed", "type", "created_date", "updated_date", "beds"]

	def to_representation(self, room):
		data = super().to_representation(room)
		image = data.get("image")

		if "image" in self.fields and image:
			data["image"] = room.image.url

		return data

	def update(self, room, validated_data):
		validated_data["number_of_bed"] = None

		for key, value in validated_data.items():
			setattr(room, key, value)
		room.save()

		return room

	def get_beds(self, room):
		beds = room.beds.all()

		return BedSerializer(beds, many=True).data


class PostSerializer(BaseSerializer):
	class Meta:
		model = Post
		fields = ["id", "name", "image", "description", "created_date", "updated_date", "room"]

	def to_representation(self, post):
		data = super().to_representation(post)
		image = data.get("image")

		if "image" in self.fields and image:
			data["image"] = post.image.url
		if "room" in self.fields:
			data["room"] = RoomSerializer(post.room).data

		return data

	def update(self, post, validated_data):
		for key, value in validated_data.items():
			setattr(post, key, value)
		post.save()

		return post


class BedSerializer(BaseSerializer):
	class Meta:
		model = Bed
		fields = ["id", "name", "price", "image", "description", "status", "created_date", "updated_date", "room"]
		extra_kwargs = {"room": {"write_only": True}}

	def to_representation(self, bed):
		data = super().to_representation(bed)
		image = data.get("image")

		if "image" in self.fields and image:
			data["image"] = bed.image.url

		return data

	def update(self, bed, validated_data):
		validated_data["price"] = None

		for key, value in validated_data.items():
			setattr(bed, key, value)
		bed.save()

		return bed

	def validate(self, data):
		room = data.get('room')
		if room:
			existing_beds_count = room.beds.count()
			number_of_beds = room.number_of_bed

			if existing_beds_count >= number_of_beds:
				raise serializers.ValidationError({"message": f"Phòng {room.name} đã đủ {number_of_beds} giường."})

		return data

from rest_framework import serializers

from base.serializers import BaseSerializer
from users import serializers as user_serializers
from rental.models import Room, Bed, Post, RentalContact, BillRentalContact, ViolateNotice


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
		room = data.get("room")

		if "image" in self.fields and image:
			data["image"] = post.image.url
		if "room" in self.fields and room:
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


class RentalContactSerializer(BaseSerializer):
	class Meta:
		model = RentalContact
		fields = ["id", "rental_number", "time_rental", "status", "created_date", "updated_date", "bed", "student"]

	def to_representation(self, rental_contact):
		data = super().to_representation(rental_contact)
		student = data.get("student")
		bed = data.get("bed")

		if "student" in self.fields and student:
			data["student"] = user_serializers.StudentSerializer(rental_contact.student).data
		if "bed" in self.fields and bed:
			data["bed"] = BedSerializer(rental_contact.bed).data

		return data


class BillRentalContactSerializer(BaseSerializer):
	class Meta:
		model = BillRentalContact
		fields = ["id", "bill_number", "total", "status", "created_date", "updated_date", "specialist", "rental_contact"]

	def to_representation(self, bill_rental_contact):
		data = super().to_representation(bill_rental_contact)
		student = data.get("student")
		specialist = data.get("specialist")
		rental_contact = data.get("rental_contact")

		if "specialist" in self.fields and specialist:
			data["specialist"] = user_serializers.SpecialistSerializer(bill_rental_contact.specialist).data
		if "rental_contact" in self.fields and rental_contact:
			data["rental_contact"] = RentalContactSerializer(bill_rental_contact.rental_contact).data

		return data


class ViolateNoticeSerializer(BaseSerializer):
	class Meta:
		model = ViolateNotice
		fields = ["id", "violate_number", "description", "created_date", "updated_date", "room"]

	def to_representation(self, violate_notice):
		data = super().to_representation(violate_notice)
		room = data.get("room")

		if "room" in self.fields and room:
			data["room"] = RoomSerializer(violate_notice.room, excludes=["beds"]).data

		return data

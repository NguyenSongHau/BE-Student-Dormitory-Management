from rest_framework import viewsets, generics, parsers, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from base import perms
from rental import serializers as rental_serializers
from rental.models import Room, Bed, Post


class RoomViewSet(viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveDestroyAPIView):
	queryset = Room.objects.filter(is_active=True).order_by("-id")
	serializer_class = rental_serializers.RoomSerializer
	parser_classes = [parsers.MultiPartParser, ]

	def get_queryset(self):
		queryset = self.queryset

		if self.action.__eq__("list"):
			name = self.request.query_params.get("name")
			queryset = queryset.filter(name__icontains=name) if name else queryset

		return queryset

	def get_permissions(self):
		if self.action in ["list", "retrieve"]:
			return [permissions.AllowAny()]

		return [perms.IsSpecialist()]

	def partial_update(self, request, pk=None):
		serializer = self.serializer_class(instance=self.get_object(), data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(data=serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveDestroyAPIView):
	queryset = Post.objects.select_related("room").filter(is_active=True).order_by("-id")
	serializer_class = rental_serializers.PostSerializer
	parser_classes = [parsers.MultiPartParser, ]

	def get_queryset(self):
		queryset = self.queryset

		if self.action.__eq__("list"):
			name = self.request.query_params.get("name")
			queryset = queryset.filter(name__icontains=name) if name else queryset

			room_type = self.request.query_params.get("type")
			queryset = queryset.filter(room__type=room_type.upper()) if room_type else queryset

		return queryset

	def get_permissions(self):
		if self.action in ["list", "retrieve"]:
			return [permissions.AllowAny()]

		return [perms.IsSpecialist()]

	def partial_update(self, request, pk=None):
		serializer = self.serializer_class(instance=self.get_object(), data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(data=serializer.data, status=status.HTTP_200_OK)


class BedViewSet(viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveDestroyAPIView):
	queryset = Bed.objects.filter(is_active=True).order_by("-id")
	serializer_class = rental_serializers.BedSerializer
	parser_classes = [parsers.MultiPartParser, ]

	def get_queryset(self):
		queryset = self.queryset

		if self.action.__eq__("list"):
			name = self.request.query_params.get("name")
			queryset = queryset.filter(name__icontains=name) if name else queryset

		return queryset

	def get_permissions(self):
		if self.action in ["list", "retrieve"]:
			return [permissions.AllowAny()]

		return [perms.IsSpecialist()]

	def partial_update(self, request, pk=None):
		serializer = self.serializer_class(instance=self.get_object(), data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(data=serializer.data, status=status.HTTP_200_OK)

from rest_framework import viewsets, generics, parsers, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from base import perms, paginators
from rental import serializers as rental_serializers
from interacts import serializers as interacts_serializers
from rental.models import Room, Bed, Post


class RoomViewSet(viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveDestroyAPIView):
	queryset = Room.objects.filter(is_active=True).order_by("-id")
	serializer_class = rental_serializers.RoomSerializer
	pagination_class = paginators.RoomPaginators
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
	pagination_class = paginators.PostPaginators
	parser_classes = [parsers.MultiPartParser, ]

	def get_queryset(self):
		queryset = self.queryset

		if self.action.__eq__("list"):
			name = self.request.query_params.get("name")
			queryset = queryset.filter(name__icontains=name) if name else queryset

			room_type = self.request.query_params.get("type")
			queryset = queryset.filter(room__type=room_type.upper()) if room_type else queryset

		queryset = queryset.prefetch_related("comments") if self.action.__eq__("comments") else queryset

		return queryset

	def get_permissions(self):
		if self.action in ["create", "partial_update", "destroy"]:
			return [perms.IsSpecialist()]

		if self.action in ["comments"] and self.request.method.__eq__("POST"):
			return [permissions.IsAuthenticated()]

		return [permissions.AllowAny()]

	@action(methods=["get", "post"], detail=True, url_path="comments")
	def comments(self, request, pk=None):
		if request.method.__eq__("POST"):
			content = request.data.get("content")
			comment = self.get_object().comments.create(content=content, user=request.user)
			serializer = interacts_serializers.CommentSerializer(comment)

			return Response(data=serializer.data, status=status.HTTP_201_CREATED)

		comments = self.get_object().comments.select_related("user").order_by("-id")

		paginator = paginators.CommentPaginators()
		page = paginator.paginate_queryset(queryset=comments, request=request)
		if page is not None:
			serializer = interacts_serializers.CommentSerializer(page, many=True)
			return paginator.get_paginated_response(serializer.data)

		serializer = interacts_serializers.CommentSerializer(comments, many=True)
		return Response(data=serializer.data, status=status.HTTP_200_OK)

	def partial_update(self, request, pk=None):
		serializer = self.serializer_class(instance=self.get_object(), data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(data=serializer.data, status=status.HTTP_200_OK)


class BedViewSet(viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveDestroyAPIView):
	queryset = Bed.objects.filter(is_active=True).order_by("-id")
	serializer_class = rental_serializers.BedSerializer
	pagination_class = paginators.BedPaginators
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

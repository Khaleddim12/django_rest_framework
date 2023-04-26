from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    thumbnail = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = ("id", "name", "price", "image", "thumbnail")

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        thumbnail = validated_data.pop('thumbnail', None)
        instance = super().create(validated_data)

        if image:
            instance.image = image
        if thumbnail:
            instance.thumbnail = thumbnail

        instance.save()
        return instance

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        thumbnail = validated_data.pop('thumbnail', None)

        instance = super().update(instance, validated_data)

        if image:
            instance.image = image
        if thumbnail:
            instance.thumbnail = thumbnail

        instance.save()
        return instance
from rest_framework import serializers
from .models import Promotion
from productcategory.models import Category


class PromotionSerializer(serializers.ModelSerializer):

    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Promotion
        fields = "__all__"

    def create(self, validated_data):
        categories = validated_data.pop("categories", [])
        promotion = Promotion.objects.create(**validated_data)

        if promotion.applies_to == "category":
            promotion.categories.set(categories)

        return promotion

    def update(self, instance, validated_data):
        categories = validated_data.pop("categories", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if categories is not None:
            instance.categories.set(categories)

        return instance
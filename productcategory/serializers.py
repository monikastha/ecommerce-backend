from rest_framework import serializers
from .models import Category, SubCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'created_at', 'updated_at']


class SubCategorySerializer(serializers.ModelSerializer):
    # 'category' field represents the read nested data object 
    category = CategorySerializer(read_only=True)
    
    # 'category_id' field handles the raw integer creation tracking on incoming POST actions
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category', 'category_id', 'created_at']
        extra_kwargs = {
            'name': {'required': True},
        }


class CategoryDetailSerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'created_at', 'updated_at', 'subcategories']
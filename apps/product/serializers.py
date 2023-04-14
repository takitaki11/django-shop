from rest_framework import serializers
from .models import Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        return [{
            'title': item.title,
            'slug': item.slug,
            'user': item.user,
            'price': item.price
        }for item in data.all()]


class ProductSerializer(serializers.ModelSerializer):
    imgs = serializers.ListField(
        child=serializers.ImageField(),
        write_only = True,
        required=False
    )

    class Meta:
        model = Product
        fields = '__all__'
        # exclude = 'полe_которoе_нужно_пропустить'
        read_only_fields = ['user', 'slug']
        list_serializer_class = ProductListSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['carousel'] = ProductImageSerializer(instance.images.all(), many=True).data
        return representation
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        imgs = validated_data.pop('imgs')
        product = Product.objects.create(**validated_data)
        images = []
        for image in imgs:
            images.append(ProductImage(product=product, image=image))
        ProductImage.objects.bulk_create(images)
        return product
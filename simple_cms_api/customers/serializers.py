from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'id',
            'name',
            'surname',
            'photo',
            'created_by',
            'updated_by',
        )
        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }

    def create(self, validated_data):
        user_creating = self.context['request'].user
        customer = Customer(**validated_data)
        customer.created_by = user_creating
        customer.save()
        return customer

    def update(self, instance, validated_data):
        user_updating = self.context['request'].user
        instance.updated_by = user_updating
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance

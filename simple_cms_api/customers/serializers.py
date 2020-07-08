from rest_framework import serializers
from .models import Customer
from django.conf import settings

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
        instance.updated_by = self.context['request'].user
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)

        if 'photo' in validated_data:
            new_photo = validated_data.get('photo')
            old_photo = instance.photo
            # if photo is supplied in validated_data then delete the old photo (if there is one) from the S3 bucket
            if old_photo:
                import boto3
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    endpoint_url=settings.AWS_S3_ENDPOINT_URL
                )
                s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=old_photo.name)

            instance.photo = new_photo

        instance.save()

        return instance

    def validate(self, data):
        uploaded_file = data.get('photo', None)
        if uploaded_file:
            if uploaded_file.content_type not in settings.ACCEPTED_PHOTO_UPLOAD_FORMATS:
                raise serializers.ValidationError(f'Trying to upload an invalid photo format. The accepted formats are: {", ".join(settings.ACCEPTED_PHOTO_UPLOAD_FORMATS)}')
            elif uploaded_file.size > settings.MAX_PHOTO_UPLOAD_SIZE:
                raise serializers.ValidationError(f'Trying to upload a photo that exceeds the maximum limit of {settings.MAX_PHOTO_UPLOAD_SIZE} bytes')

        return data
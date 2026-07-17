import base64
from email.mime import image
from typing import Any, Dict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers


from core_apps.common.models import ContentView
from .models import Profile, NextOfKin
# from .tasks import upload_photo_to_cloudinary

User = get_user_model()

class UUIDField(serializers.Field):
    def to_representation(self, value:str)->str:
        return str(value)


class NextOfKinSerializer(serializers.ModelSerializer):
    id = UUIDField(read_only=True)
    country = CountryField(name_only=True)
    phone_number = PhoneNumberField()

    class Meta:
        model = NextOfKin
        exclude = ["profile"]

    def create(self, validated_data: dict) -> NextOfKin:
        profile = self.context.get("profile")
        if not profile:
            raise serializers.ValidationError("Profile context is required")

        return NextOfKin.objects.create(profile=profile, **validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    id = UUIDField(read_only=True)
    first_name = serializers.CharField(source="user.first_nam")
    last_name = serializers.CharField(source="user.last_name")
    username = serializers.ReadOnlyField(source="user.username")
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.ReadOnlyField(source="user.full_name")
    id_no = serializers.ReadOnlyField(source="user.id_no")
    date_joined = serializers.DateTimeField(read_only=True, source="user.date_joined")
    country_of_birth = CountryField(name_only=True)
    country = CountryField(name_only=True)
    phone_number = PhoneNumberField()
    next_of_kin = NextOfKinSerializer(many=True, read_only=True)
    photo = serializers.ImageField(write_only=True, required=False)
    is_photo = serializers.ImageField(write_only=True, required=False)
    signature_photo = serializers.ImageField(write_only=True, required=False)
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        exclude = ["id"]

    def validate(self, attrs:Dict[str, Any])->Dict[str, Any]:
        id_issue_date = attrs.get("id_issue_date")
        id_expiry_date = attrs.get("id_expiry_date")

        if id_issue_date and id_expiry_date and id_expiry_date <= id_issue_date:
            raise serializers.ValidationError(
                {
                    "id_expiry_date": "ID expiry date must be after issue date "
                }
            )
        return attrs

    def to_representation(self, instance: Profile)-> dict :
        representation = super().to_representation(instance)

        representation["next_of_kin"] = NextOfKinSerializer(
            instance.next_of_kin.all(), many=True
        ).data

        return representation

    def update(self, instance:Profile, validated_data:dict)-> Profile:
        user_data = validated_data.pop("user", {})

        if user_data:
            for attr, value in user_data.items():
                if attr not in ["email", "username"]:
                    setattr(instance.user, attr, value)
            instance.user.save()

        photo_to_upload = {}
        for field in ["photo","is_photo","signature_photo"]:
            if field in validated_data:
                photo = validated_data.pop(field)
                if photo.size >= settings.MAX_UPLOAD_SIZE:
                    temp_file = default_storage.save(
                       f"temp_{instance.id}_{field}.jpg", ContentFile(photo.read())
                   )
                    temp_file_path = default_storage.path(temp_file)
                    photo_to_upload[field] = {"type": "file", "path": temp_file_path}

                else:
                   image_content = photo.read()
                   encoded_image = base64.b64encode(image_content).decode("utf-8")
                   photo_to_upload[field] = {"type": "bas64", "path": temp_file_path}

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # if photo_to_upload:
            # upload_photos_to_cloudinary.delay(str(instance.id), photo_to_upload)

        return  instance

    def get_view_count(self, obj:Profile)-> int:
        content_type = ContentType.objects.get_for_model(obj)
        return ContentView.objects.filter(content_type=content_type, object_id=obj.id).count()

class ProfileListSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.ReadOnlyField(source="user.full_name")
    photo = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Profile
        field = [
            "full_name",
            "username",
            "photo",
            "gender",
            "nationality",
            "country_of_birth",
            "email",
            "phone_number",
        ]

    def get_photo(self, obj: Profile) -> str |  None:
        try:
            return  obj.photo.url
        except AttributeError:
            return None






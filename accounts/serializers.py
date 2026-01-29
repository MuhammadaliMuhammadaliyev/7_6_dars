from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class SignUpSerializer(serializers.ModelSerializer):
    confirm_pass = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'password', 'confirm_pass']
        
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_pass = attrs.get('confirm_pass')
        if password is None or confirm_pass is None or password != confirm_pass:
            raise ValidationError({"success": False, 'message': 'Parollar toliq kiritilmagan'})
        
        return attrs
        
    def create(self, validated_data):
        validated_data.pop('confirm_pass')
        user = User.objects.create_user(**validated_data)
        # user.set_password(validated_data['password'])
        # user.save()
        return user
    
    
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", 'username']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise ValidationError({"success": False, "message": "Yangi parollar mos emas"})

        return attrs

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class CreateUserSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField()

    def create(self, validated_data):
        try:
            user = User.objects.filter(username=validated_data.get('username'))
            if len(user) > 0:
                raise serializers.ValidationError(("Username already exists"))
        except User.DoesNotExist:
            pass

        if not validated_data.get('email'):
            raise serializers.ValidationError(("Empty email"))

        if not validated_data.get('password') or not validated_data.get('confirm_password'):
            raise serializers.ValidationError(("Empty Password"))

        if validated_data.get('password') != validated_data.get('confirm_password'):
            raise serializers.ValidationError(("Mismatch"))

        del validated_data['confirm_password']

        user = User.objects.create_user(**validated_data)

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password' ,'confirm_password' , 'email')
        extra_kwargs = {'password': {'write_only': True},'confirm_password': {'read_only': True}}

class UpdateUserSerializer(serializers.ModelSerializer):

    original_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def update(self, validated_data):
        try:
            user = User.objects.filter(username=validated_data.get('username'))
            if not user.check_password(validated_data.get('original_password')):
                raise serializers.ValidationError(("password wrong"))
        except User.DoesNotExist:
            pass

        if not validated_data.get('password') or not validated_data.get('confirm_password'):
            raise serializers.ValidationError(("Empty Password"))

        if validated_data.get('password') != validated_data.get('confirm_password'):
            raise serializers.ValidationError(("Mismatch"))

        del validated_data['confirm_password']
        del validated_data['original_password']

        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data.get('password'))

        return user

    class Meta:
        model = User
        fields = ('username', 'original_password', 'password' ,'confirm_password')
        extra_kwargs = {'password': {'write_only': True},'confirm_password': {'read_only': True}}

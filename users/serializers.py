from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class MgrSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=False)
    confirm_password = serializers.CharField(required=False)

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
        del validated_data['confirm_password']
        user = User.objects.create_user(**validated_data)

        return user
        
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.password = make_password(validated_data.get('new_password', instance.password))

        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'password','new_password' ,'confirm_password' , 'email')
        extra_kwargs = {'password': {'write_only': True},
        'new_password': {'write_only': True},
        'confirm_password': {'read_only': True}}

class UserSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()
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
    def update(self, instance, validated_data):
        if not instance.check_password(validated_data.get('password')):
            raise serializers.ValidationError(("Old Password wrong!"))

        if not validated_data.get('new_password') or not validated_data.get('confirm_password'):
            raise serializers.ValidationError(("Empty Password"))

        if validated_data.get('new_password') != validated_data.get('confirm_password'):
            raise serializers.ValidationError(("Mismatch"))

        instance.email = validated_data.get('email', instance.email)
        instance.password = make_password(validated_data.get('new_password', instance.password))
        
        del validated_data['new_password']
        del validated_data['confirm_password']

        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'password','new_password' ,'confirm_password' , 'email')
        extra_kwargs = {'password': {'write_only': True},
        'new_password': {'write_only': True},
        'confirm_password': {'read_only': True}}
        

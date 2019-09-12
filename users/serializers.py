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


    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user

    # class Meta:
    #     model = User
    #     # ('id', 'username', 'password' , 'email')
    #     fields = ('id','username', 'password', 'first_name', 'last_name' ,'email' , 'is_active')
    #     extra_kwargs = {
    #         'password': {'write_only': True}
    #     }


# from rest_framework import generics, permissions, serializers
# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

# from django.contrib.auth.models import User, Group

# class RegistrationSerializer(serializers.ModelSerializer): 
#     class Meta: 
#         model = User 
#         fields = ('username', 'password')

# class RegisterSerializer(serializers.ModelSerializer):
#     confirm_password = serializers.CharField()

#     def validate(self, data):
#         try:
#             user = User.objects.filter(username=data.get('username'))
#             if len(user) > 0:
#                 raise serializers.ValidationError(("Username already exists"))
#         except User.DoesNotExist:
#             pass

#         if not data.get('password') or not data.get('confirm_password'):
#             raise serializers.ValidationError(("Empty Password"))

#         if data.get('password') != data.get('confirm_password'):
#             raise serializers.ValidationError(("Mismatch"))

#         del data['confirm_password']

#         return data

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'password' ,'email' , 'confirm_password', 'is_active')
#         extra_kwargs = {'confirm_password': {'read_only': True}}
# # first we define the serializers
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'email', "first_name", "last_name")

# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ("name", )

# # Create the API views
# class UserList(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetails(generics.RetrieveAPIView):
#     permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class GroupList(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated, TokenHasScope]
#     required_scopes = ['groups']
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
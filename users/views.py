from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser , IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets


from users.serializers import CreateUserSerializer

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

import requests
# Create your views here.



CLIENT_ID = '<client-id>'
CLIENT_ID = '446LXZnjQrad8LxtMQnUTHlUsBn6bN2DPY2SyG3d'
# EkneVcK1AwN7VrvvfhFKumgSRWXrrFfHMb3xcqWK
CLIENT_SECRET = '<client-secret>'
CLIENT_SECRET = '9S8YJekBNbVdgjvmvuU8BnPjIilhYl3IyiM0z5gecgLa9K9RhhtVALH9KYEi6xlsuQ37iDDinK4BTOySmjSQ0KzholoXZaGeEeCae0CtXHtf2ejyA5537iLcPSJ0w3rN'
# 89DByPJNwHxDOW3PeNsqFZIPvdpZdAczPbik5eii5GG6uivDwxDOOfiiiOzVFK0Yay1fuaFrndI47F5mqDnnMYXdAv9t6ouVABTJJdTPPix0rQ78aF226rkpkEdjfeLy
ROOT = 'http://localhost:8000'

class AdminMgr(APIView):
    permission_classes = [IsAdminUser]
    def get(self , request):
        # show list
        userlist = User.objects.All()
        return ''
    def post(self , request):
        # register user
        serializer = CreateUserSerializer(data=request.data) 
        # Validate the data
        if serializer.is_valid():
            # If it is valid, save the data (creates a user).
            serializer.save() 
            # Then we get a token for the created user.
            # This could be done differentley 
            r = requests.post(ROOT+'/o/token/', 
                data={
                    'grant_type': 'password',
                    'username': request.data['username'],
                    'password': request.data['password'],
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                },
            )

            return Response(r.json())
        return Response(serializer.errors)

    def put(self , request):
        # update user
        return ''
    def delete(self , request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        try:
            u = User.objects.get(username = request.data['username'])
            u.delete()
            messages.success(request, "The user is deleted")            
        except User.DoesNotExist:
            messages.error(request, "User doesnot exist")
            return Response('not exist')
        return Response('success')


class UserAccount(APIView):
    permission_classes = [AllowAny]

    def post(self , request):
        # register user
        serializer = CreateUserSerializer(data=request.data) 
        # Validate the data
        if serializer.is_valid():
            # If it is valid, save the data (creates a user).
            serializer.save() 
            # Then we get a token for the created user.
            # This could be done differentley 
            r = requests.post(ROOT+'/o/token/', 
                data={
                    'grant_type': 'password',
                    'username': request.data['username'],
                    'password': request.data['password'],
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                },
            )

            return Response(r.json())
        return Response(serializer.errors)

    def put(self , request):
        # update user
        return ''

    def delete(self , request):
        # logout
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        return 'logout'

class UserToken(APIView):
    # CLIENT_ID = '<client-id>'
    # CLIENT_SECRET = '<client-secret>'
    permission_classes = [AllowAny]

    def post(self , request):
            r = requests.post(
            ROOT+'/o/token/', 
                data={
                    'grant_type': 'password',
                    'username': request.data['username'],
                    'password': request.data['password'],
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                },
            )
            return Response(r.json())

    def put(self , request):
        if not request.data.get('refresh_token',''):
            return Response('Not found the refresh_token',status = 401)
        r = requests.post(
        ROOT+'/o/token/', 
            data={
                'grant_type': 'refresh_token',
                'refresh_token': request.data['refresh_token'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json())

    def delete(self ,request):
        if not request.data.get('token',''):
            return Response('Not found the refresh_token',status = 401)
        r = requests.post(
                ROOT+'/o/revoke_token/', 
                data={
                    'token': request.data['token'],
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                },
            )
            
        # If it goes well return sucess message (would be empty otherwise) 
        if r.status_code == requests.codes.ok:
            return Response({'message': 'token revoked'}, r.status_code)
        # Return the error if it goes badly
        return Response(r.json(), r.status_code)

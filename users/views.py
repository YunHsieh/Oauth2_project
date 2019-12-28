from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser , IsAuthenticated
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import viewsets, status

from users.serializers import *
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse, QueryDict
from django.contrib.auth.models import update_last_login

from rest_framework.schemas import get_schema_view
from rest_framework_swagger import renderers

import requests
import json

import coreapi
from rest_framework.schemas import AutoSchema

ROOT = 'http://localhost:8000'
CLIENT_ID = 'TEESPmHm97K0vxSCjhg576CtuaJg0lMObBbvuTdf'
CLIENT_SECRET = '9CvVvd2Jj48rYAM8rzPKizPCXnrxJUsqtWj8X5S6DJ6dfPreNfY4SQ4VHKfxn8cEV8PaFj0HEUVn2JkIILSWjC4j5YFs9b6TXJF6D73xX2v1CEJEg7pyhH8jcJtDwIRv'

class AdminMgr(APIView):
    authentication_classes = [OAuth2Authentication ]
    permission_classes = [IsAdminUser]
    schema = AutoSchema(manual_fields=[
        # coreapi.Field('username', location='form'),
        # coreapi.Field('password', location='form'),
        # coreapi.Field('client_id', location='form'),
        # coreapi.Field('client_secret', location='form'),
        # coreapi.Field('refresh_token', location='form'),
    ])

    def get(self , request):
        # show list
        userlist = User.objects.values('id', 'is_superuser', 'username', 'first_name' ,'last_name', 'email' ,'is_active', 'last_login')

        return JsonResponse(list(userlist), safe=False)

    def post(self , request):
        # register user
        print(request.data)
        serializer = MgrSerializer(data=request.data) 
        if not request.data.get('groupname',''):
            return Response('No parameter groupname', status=status.HTTP_400_BAD_REQUEST)

        for _group in request.data['groupname'].split(','):
            if not Group.objects.get(name=_group):
                return Response('No find this groupname : %s' % (_group), status=status.HTTP_400_BAD_REQUEST)

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
            # add to this group
            new_user = User.objects.get(username=request.data['username'])

            for _group in request.data['groupname'].split(','):
                group = Group.objects.get(name=_group)
                new_user.groups.add(group)

            return Response(r.json())
        return Response(serializer.errors)

    def put(self , request):
        serializer = MgrSerializer(User.objects.get(username=request['POST'].get('username','')), data=request.data)
        if serializer.is_valid():
            serializer.save()
        # update user
        return ''
    def delete(self , request):
        u = User.objects.get(username = request.data['username'])
        try:
            u.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        try:
            u.delete()
            messages.success(request, "The user is deleted")            
        except User.DoesNotExist:
            messages.error(request, "User doesnot exist")
            return Response('not exist')
        return Response('success')


class UserAccount(APIView):
    authentication_classes = [OAuth2Authentication ]
    permission_classes = [AllowAny ]
    serializer_class = UserSerializer
    schema = AutoSchema(manual_fields=[
        coreapi.Field('username', location='form'),
        coreapi.Field('password', location='form'),
        # coreapi.Field('client_id', location='form'),
        # coreapi.Field('client_secret', location='form'),
        coreapi.Field('refresh_token', location='form'),
    ])

    # update user
    def put(self , request):
        _dict={ _key:_val[0] for _key,_val in dict(request.data).items()}
        _dict['username'] = request.user.username

        serializer = UserSerializer(User.objects.get(pk=request.user.id), data=_dict)
        if serializer.is_valid():
            serializer.save()

        return Response("succeed")
        
        
    def delete(self , request):
        # logout
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        return Response('logout')

class UserToken(APIView):
    authentication_classes = [OAuth2Authentication ]
    permission_classes = [AllowAny ]

    schema = AutoSchema(manual_fields=[
        coreapi.Field('username', location='form'),
        coreapi.Field('password', location='form'),
        # coreapi.Field('client_id', location='form'),
        # coreapi.Field('client_secret', location='form'),
        coreapi.Field('refresh_token', location='form'),
        coreapi.Field('delete_token', location='form'),
    ])
    # get token
    def get(self, request):
        
        if request.user.is_anonymous:
             raise PermissionDenied()

        user_info = {}
        user_info['user'] = request.user.username
        user_info['email'] = request.user.email
        user_info['last_logined'] = request.user.last_login
        user_info['date_joined'] = request.user.date_joined
        update_last_login(None,request.user)
        return JsonResponse(user_info)
        

    def post(self, request):
        """
        This is add the function.
        ---
            parameters:
            - name : username 
              description: kpi name
              required: true
              type: string
              paramType: query
            - name : password
              description: KPI category
              required: true
              type: string
              paramType: query
            - name : client_id 
              description: KPI rename
              required: true
              type: string
              paramType: query
            - name : client_secret
              description: KPI version
              required: true
              type: string
              paramType: query
        """ 
        r = requests.post(
        ROOT+'/o/token/', 
            data={
                    'grant_type': "password",
                    'username': request.data['username'],
                    'password': request.data['password'],
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json())

    # refresh token
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

    # delete token
    def delete(self ,request):

        if not request.META.get('HTTP_AUTHORIZATION',''):
            return JsonResponse({'message':'error'}, status=status.HTTP_400_BAD_REQUEST)

        r = requests.post(
                ROOT+'/o/revoke_token/', 
                data={
                    'token': request.META.get('HTTP_AUTHORIZATION').split(' ')[1],
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                },
            )

        if r.status_code == requests.codes.ok:
            return Response({'message': 'token revoked'}, r.status_code)
        return Response(r.json(), r.status_code)

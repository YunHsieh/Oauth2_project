from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser , IsAuthenticated 
from django.contrib.auth.models import User

from collections import defaultdict

class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    permission_classes = [IsAuthenticated ]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        users_info = defaultdict(list)
        for _userinfo in User.objects.all():
        	users_info['username'].append(_userinfo.username)
        	users_info['last_login'].append(_userinfo.last_login)
        	if _userinfo.is_superuser == 1:
        		users_info['is_staff'].append('admin')
        	else:
        		
        		users_info['is_staff'].append('user')
        	users_info['email'].append(_userinfo.email)
        return Response(users_info)
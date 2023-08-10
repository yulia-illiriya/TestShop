from django.shortcuts import render
from django.contrib.auth import logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

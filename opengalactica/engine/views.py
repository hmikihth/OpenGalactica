from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def auth_status(request):
    return Response({'is_authenticated': request.user.is_authenticated})


from rest_framework.views import APIView
from django.contrib.auth import authenticate, login

class CustomLoginView(APIView):
    permission_classes = [AllowAny]  # Allow any user (authenticated or not)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"})
        else:
            return Response({"error": "Invalid credentials"}, status=400)


from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

@method_decorator(csrf_protect, name='dispatch')
class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can log out

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"})
        
        
from django.views.decorators.csrf import ensure_csrf_cookie

@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):
    return Response({'message': 'CSRF cookie set'})
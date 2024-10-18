# views.py
import requests
from rest_framework.decorators import api_view
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from user_management.models import CustomUser
from django.contrib.auth import login as auth_login
from rest_framework import status
from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated

REDIRECT_URI = 'http://localhost:8000/noexist/callback'
CLIENT_ID = 'u-s4t2ud-34d662ce43a4ee1a1ea0cfd6c5237edb098bcb4111806c30d5f52ca800cb5b6d'
CLIENT_SECRET = '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'

def login(request):
    # Step 1: Redirect to the authorization URL
    auth_url = (
        f'https://api.intra.42.fr/oauth/authorize?client_id={CLIENT_ID}'
        f'&redirect_uri={REDIRECT_URI}&response_type=code'
    )
    return redirect(auth_url)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def callback(request):

    # Step 2: Exchange the authorization code for an access token
    code = request.GET.get('code')
    if not code:
        return Response({"detail": "Authorization code is missing."}, status=status.HTTP_400_BAD_REQUEST)

    token_url = 'https://api.intra.42.fr/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code,
    }
    # Requesting the access token
    response = requests.post(token_url, data=data)
    print(response.text)
    response_data = response.json()
    # Check if the response contains the access token
    if response.status_code != 200 or 'access_token' not in response_data:
        return Response({
            "detail": "Failed to obtain access token.",
            "error": response_data.get('error', 'Unknown error'),
        }, status=status.HTTP_400_BAD_REQUEST)

    # Handle access token and refresh token
    access_token = response_data['access_token']
    refresh_token = response_data.get('refresh_token')

    # Use the access token to access the API
    api_url = 'https://api.intra.42.fr/v2/me'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    # Request user data from the API
    api_response = requests.get(api_url, headers=headers)
    print(api_response.text)
    if api_response.status_code != 200:
        return Response({
            "detail": "Failed to retrieve user data.",
            "error": api_response.json().get('error', 'Unknown error'),
        }, status=status.HTTP_400_BAD_REQUEST)

    user_data = api_response.json()
    id = user_data.get('id')
    username = user_data.get('login')
    avatar_url = user_data.get('image_url')
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        # User doesn't exist, create a new one
        user = CustomUser.objects.create_user(
            id = id,
            username=username,
            avatar=avatar_url,
        )
        user.set_unusable_password()  # Since you won't be using passwords
        user.save()
    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    response = Response({
        "detail": "Login successful",
        "id": user.id,
        "username": user.username,
        "avatar": avatar_url,
        "access_token": access_token,  # Optional, can be sent if needed
    }, status=status.HTTP_200_OK)

    # Set refresh token in HTTP-only cookie
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,  # Prevents JavaScript access
        secure=True,    # Use True if using HTTPS
        samesite='Lax', # Can be adjusted based on your CSRF protection needs
        expires=timezone.now() + timedelta(days=30)  # Set expiration as needed
    )
    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_access_token(request):
    refresh_token = request.COOKIES.get('refresh_token')  # Get the refresh token from the cookie

    if not refresh_token:
        return Response({"detail": "Refresh token is missing."}, status=status.HTTP_400_BAD_REQUEST)

    # Validate the refresh token (add your logic here)
    # If valid, generate a new access token
    user = request.user  # Get the user from the request
    if user:
        # Generate new access token
        new_access_token = generate_new_access_token(user)  # Implement this function
        return Response({"access_token": new_access_token}, status=status.HTTP_200_OK)
    
    return Response({"detail": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)
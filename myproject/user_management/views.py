from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .serializers import MatchSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterView(generics.CreateAPIView):
  queryset = CustomUser.objects.all()
  serializer_class = RegisterSerializer
  permission_classes = [permissions.AllowAny]
class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,    
                samesite='Lax',
            )
            return response
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class RecordMatchView(APIView):
  permission_classes = [permissions.IsAuthenticated]  # Add this line
  authentication_classes = [JWTAuthentication]

  def post(self, request, *args, **kwargs):
      data = request.data
      match = Match.objects.create(
          player1_id=data['player1_id'],
          player2_id=data['player2_id'],
          winner_id=data['winner_id'],
          score=data.get('score', '')
      )
      serializer = MatchSerializer(match)
      return Response(serializer.data, status=status.HTTP_201_CREATED)

class MatchHistoryView(APIView):
  permission_classes = [permissions.IsAuthenticated]  
  authentication_classes = [JWTAuthentication]
  def get(self, request, *args, **kwargs):
      matches = Match.objects.filter(player1=request.user) | Match.objects.filter(player2=request.user)
      serializer = MatchSerializer(matches, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
  
class ProfileView(generics.RetrieveUpdateAPIView):
  permission_classes = [permissions.IsAuthenticated]  
  authentication_classes = [JWTAuthentication]
  queryset = CustomUser.objects.all()
  serializer_class = UserSerializer
  def get_object(self):
      return self.request.user
  
class AddFriendView(APIView):
  permission_classes = [permissions.IsAuthenticated] 
  authentication_classes = [JWTAuthentication]
  def post(self, request, *args, **kwargs):
      friend_id = request.data.get('friend_id')
      try:
          friend = CustomUser.objects.get(id=friend_id)
          request.user.friends.add(friend)
          return Response({'detail': 'Friend added successfully.'}, status=status.HTTP_200_OK)
      except CustomUser.DoesNotExist:
          return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

class FriendListView(APIView):
  permission_classes = [permissions.IsAuthenticated]
  authentication_classes = [JWTAuthentication]
  def get(self, request, *args, **kwargs):
      friends = request.user.friends.all()
      serializer = UserSerializer(friends, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
  
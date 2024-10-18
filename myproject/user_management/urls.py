from django.urls import path
from .views import RegisterView, LoginView
from .views import RecordMatchView, MatchHistoryView, AddFriendView, FriendListView, ProfileView

urlpatterns = [
  path('register/', RegisterView.as_view(), name='register'),
  path('login/', LoginView.as_view(), name='login'),
  path('profile/', ProfileView.as_view(), name='profile'),
  path('add-friend/', AddFriendView.as_view(), name='add-friend'),
  path('friends/', FriendListView.as_view(), name='friend-list'),
  path('record/', RecordMatchView.as_view(), name='record-match'),
  path('history/', MatchHistoryView.as_view(), name='match-history'),
]
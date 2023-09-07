from django.urls import path
from .views import UserRegistrationView, GenerateTelegramTokenView, SendMessageView, MessageListView, MessageCreateView, UserLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register_user'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('generate-token/', GenerateTelegramTokenView.as_view(), name='generate_telegram_token'),
    path('send-message/', SendMessageView.as_view(), name='send_message'),
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('messages/create/', MessageCreateView.as_view(), name='message-create'),  
]

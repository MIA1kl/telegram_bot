from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from .telegram_bot import get_telegram_bot
from .models import Message, Token, CustomUser
from .serializers import MessageSerializer, CustomUserSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer 

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.validated_data
            return Response(response_data['tokens'], status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateTelegramTokenView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.token})


class SendMessageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def post(self, request):
        user = request.user
        body = request.data.get('message')

        if not body:
            return Response({'message': 'Please provide a message.'}, status=status.HTTP_400_BAD_REQUEST)

        bot = get_telegram_bot(user)
        if not bot:
            return Response({'message': 'Telegram bot token is missing. Generate one first.'}, status=status.HTTP_400_BAD_REQUEST)

        chat_id = user.telegram_token  
        if chat_id:
            bot.send_message(chat_id, f"{user.username}, I received a message from you:\n{body}")

        message = Message.objects.create(user=user, body=body)

        return Response({'message': f"{user.username}, I received a message from you:\n{body}"})


class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageListView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

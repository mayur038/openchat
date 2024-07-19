from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from .models import Box, Messages
import uuid
from django.core.mail import send_mail
from django.conf import settings
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])
        user.save()
        email = validated_data['email']
        se = send_mail(
            'Welcome to OpenChat!',
            'Thank you for signing up for OpenChat. We are glad to have you! <br> you can send and Receive message anonymously..',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        print(email)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Both username and password are required")
        data['user'] = user
        return data

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = '__all__'
        extra_kwargs = {
            'username': {'required': False},
            'chatcode': {'required': True}
        }

    def validate(self, data):
        request = self.context.get('request')
        if not request or not hasattr(request, 'auth'):
            raise serializers.ValidationError("Request context with auth token is required.")

        token_key = request.auth.key
        try:
            token = Token.objects.get(key=token_key)
            user = User.objects.get(id=token.user_id)
        except (Token.DoesNotExist, User.DoesNotExist):
            raise serializers.ValidationError("Invalid token or user does not exist.")

        unique_id = uuid.uuid4()
        short_uuid = str(unique_id)[:6]

        data['username'] = user
        chatcode= data.get('chatcode')
        data['chatcode'] = chatcode
    
        return data

    def create(self, validated_data):
        return Box.objects.create(**validated_data)

class JoinSerializer(serializers.Serializer):
    chatcode = serializers.CharField(required=True)

    class Meta:
        model = Box
        fields = '__all__'
        extra_kwargs = {
            'username': {'required': False},
            'chatcode': {'required': True}
        }

    def validate(self, data):
        request = self.context.get('request')
        if not request or not hasattr(request, 'auth'):
            raise serializers.ValidationError("Request context with auth token is required.")
        
        chatcode = data.get('chatcode')
        if chatcode is None or not Box.objects.filter(chatcode=chatcode).exists():
            raise serializers.ValidationError("Invalid chatcode: This chatcode does not exist.")
        
        return data 

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['username', 'Message', 'Time', 'chatcode']
        extra_kwargs = {
            'username': {'required': False},
            'chatcode': {'required': False},
            'Message': {'required': True},
            'Time': {'required': False},
        }

    def create(self, validated_data):
        validated_data['Time'] = timezone.now()
        return Messages.objects.create(**validated_data)

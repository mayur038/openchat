from django.utils import timezone
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer, LoginSerializer, MessageSerializer, UserModelSerializer, JoinSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid

User = get_user_model()
@csrf_exempt
def error(request):
    return render(request, 'error.html')

@csrf_exempt
def indes(request):
    return render(request, 'index.html')

@csrf_exempt
def createse(request):
    return render(request, 'CreateJoin.html')

@csrf_exempt
def message(request, chatcode):
    return render(request, 'message.html', {'chatcode': chatcode})

@csrf_exempt
def generate(request):
    unique_id = uuid.uuid4()
    short_uuid = str(unique_id)[:6]
    return JsonResponse({'chatcode': short_uuid, "status": status.HTTP_200_OK, "ok": True})

class Register(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
        
            return JsonResponse({"token": str(token), "status": status.HTTP_200_OK, "ok": True})
        return render(request, 'error.html', {"message":serializer.errors})
    
class Login(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            print(token)
            return JsonResponse({"token": str(token), "status": status.HTTP_200_OK, "ok": True})
        return render(request, 'error.html', {"message":serializer.errors})
    
class CreateRoom(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request):
        serializer = UserModelSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            chatcode = serializer.validated_data['chatcode']
            return JsonResponse({"chatcode": chatcode, "redirect": "message"}, status=status.HTTP_201_CREATED)
        return render(request, 'error.html', {"message":serializer.errors})
class JoinRoom(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request):
        serializer = JoinSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            chatcode = serializer.validated_data['chatcode']
            dynamic_url = f'/message/{chatcode}/'
            return redirect('message', chatcode=chatcode)
        return render(request, 'error.html', {"message":serializer.errors})
class Chat(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self, request, chatcode):
        messages = Messages.objects.filter(chatcode__chatcode=chatcode)
        serializer = MessageSerializer(messages, many=True)
        print(serializer.data)
        return JsonResponse({"Message": serializer.data})

    @csrf_exempt
    def post(self, request, chatcode):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            box = get_object_or_404(Box, chatcode=chatcode)
            serializer.save(username=request.user, chatcode=box, Time=timezone.now())
            dynamic_url = f'/message/{chatcode}/'
            return JsonResponse({'redirect': dynamic_url}, status=200)
        print(serializer.errors)
        return render(request, 'error.html', {"message":serializer.errors})
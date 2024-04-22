from django.views.decorators.csrf import ensure_csrf_cookie
from .models import User
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from project import file_operations
from account import jwt
from datetime import datetime, timedelta, timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse

@csrf_exempt
@api_view(['POST'])
def Authentication(request):
    token = request.COOKIES.get('token')
    if token:
        try:
            JWT_str = jwt.decode_jwt_token(token)
            user = User.objects.get(email=JWT_str['email'])
            return Response({'message': 'Success','userName': user.username, 'email':JWT_str['email']})
            # return Response({'message': 'Success','userName': JWT_str['user'], 'email':JWT_str['email']})
        except Exception as e:
            return Response({'error': 'Invalid token'})
    else:
        return Response({'error': 'Token not found in cookies'})
    
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        # print(request.data.get('name'))
        # input('stop')
        existing_user = User.objects.filter(
            email=request.data.get('email')).first()
        if existing_user is None:

            user = User(username=request.data.get('name'), email=request.data.get(
                'email'), password=request.data.get('password'))

            file_operations.create(user.email)
            
            user.save()
            return Response({'message': 'Successfully Registered'})
        else:
            return Response({'error': 'User with the same email already exists'})
    else:
        return Response({'error': 'Something went wrong'})

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if user.password == password:
                JWT = jwt.generate_jwt_token(user.username, user.email, user.id)
                JWT_str = JWT.decode('utf-8') if isinstance(JWT, bytes) else JWT
                response = Response({'success': 'Login Successfull.'})
                response.set_cookie('token', JWT_str, max_age=3600) 
                return response
            else:
                return Response({'error': 'Incorrect password'})
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'})
    else:
        return Response({'error': 'Method not allowed'})
    
@api_view(['GET'])
def logout(request):
    if request.method == 'GET':
        token = request.COOKIES.get('token')
        if token:
            try:
                response = Response({'message': 'Success'})
                response.delete_cookie('token')
                return response
            except Exception as e:
                return Response({'error': 'Invalid token'})
        else:
            return Response({'error': 'Token not found in cookies'})
    else:
        return Response({'error': 'Method not allowed'})
    

@api_view(['POST'])
def updateProfile(request):
    if request.method == 'POST':
        name = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if password is '':
            user = User.objects.get(email=email)
            user.username = name
            user.email = email
            user.save()
            return Response({'message': 'Successfully Updated'})
        else:
            user = User.objects.get(email=email)
            user.username = name
            user.email = email
            user.password = password
            user.save()
            return Response({'message': 'Successfully Updated'})
    else:
        return Response({'error': 'Something went wrong'})
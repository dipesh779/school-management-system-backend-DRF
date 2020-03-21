from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MyUserSerializer, LoginSerializer, ResetPasswordSerializer, MyUserListSerializer
from .models import MyUser
from rest_framework_simplejwt.tokens import RefreshToken
from .create_response import create_response
from django.contrib.auth import get_user_model
from rest_framework import generics


class CreateUserView(generics.ListCreateAPIView):
    model = get_user_model()
    permission_classes = [IsAdminUser, ]
    serializer_class = MyUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = MyUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'success', 'status': status.HTTP_200_OK, 'result': serializer.data})
        return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})

    def get(self, request):
        user = MyUser.objects.all()
        serializer = MyUserListSerializer(user, many=True)
        return Response({'message': 'success', 'status': status.HTTP_200_OK, 'response': serializer.data})


class LoginView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.validated_data)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                context = dict()
                context['user'] = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
                context['refresh_token'] = str(refresh)
                context['access_token'] = str(refresh.access_token)
                return Response(create_response(True, data=context), status=status.HTTP_200_OK)
            else:
                return Response(create_response(False, err_name="Incorrect Credentials",
                                                err_message=f'Authenticate returned '
                                                            f'None'),
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(create_response(False, err_name="Provided data didn't "
                                                            "Validate",
                                            err_message=f'{serializer.errors}'),
                            status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            password = serializer.validated_data['password']
            user.set_password(password)
            user.save()

            return Response(create_response(True, data=f'password changed successfully'
                                                       f' {user.id}'),
                            status=status.HTTP_200_OK)
        else:
            return Response(create_response(False, err_name='Invalid Data',
                                            err_message=f'{serializer.errors}'),
                            status=status.HTTP_400_BAD_REQUEST)

import random
from .serializers import SignUpSerializer, ProfileUpdateSerializer, ChangePasswordSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
from .utility import send_simple_email, check_email
from .models import VerifyCodes
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model
from .models import UserVerifyCodes

User = get_user_model()

# Create your views here.

class SignUpView(APIView):
    serializer_class = SignUpSerializer
    queryset = User
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        data = {
            'status': status.HTTP_201_CREATED,
            'username': serializer.data['username'],
            'message': 'Akkount yaratildi'
        }
        return Response(data=data)

        
class LoginView(APIView):
    def post(self, request):
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        
        user = User.objects.filter(username=username).first()
        if user is None:
            raise ValidationError({"status": status.HTTP_400_BAD_REQUEST, 'message': 'Bizda bunaqa user mavjud emas'})
        user = user.check_password(password)
        if not user:
            raise ValidationError({"status": status.HTTP_400_BAD_REQUEST, 'message': 'PArolingiz xato'})
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise ValidationError({"status": status.HTTP_400_BAD_REQUEST, 'message': 'Bizda bunaqa user mavjud emas'})
        
        refresh = RefreshToken.for_user(user)
        
        data = {
            'status': status.HTTP_200_OK,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Siz tizimga kirdingiz'
        }
        
        return Response(data=data)
        
        
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request):
        refresh = self.request.data.get('refresh_token')
        refresh = RefreshToken(refresh)
        refresh.blacklist()
        data = {
            'success': True,
            'message': 'Siz tizimdan chiqdingiz'
        }
        return Response(data)
        


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = self.request.user
        
        data = {
            'status': status.HTTP_200_OK,
            'username': user.username,
            'first_name': user.first_name
        }
        return Response(data)
    
    
class ProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        serializer = ProfileUpdateSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            
            data = {
                'status': status.HTTP_200_OK,
                'username': user.username,
                'first_name': user.first_name,
                'message': 'Malumotlar yangilandi'
            }
            return Response(data)
        data = {
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'ERROR'
        }
        return Response(data)
    
    
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        # eski parol tekshirish
        if not user.check_password(old_password):
            raise ValidationError({"status": status.HTTP_400_BAD_REQUEST, "message": "Eski parol xato"})

        # yangi parolni o'rnatish
        user.set_password(new_password)
        user.save()

        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Parol yangilandi. Qayta login qiling."
        })


class ForgotView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = self.request.data.get('email')
        email = check_email(email)
        if email:
            user = User.objects.filter(email=email).first()
            if user is None:
                raise ValidationError('Bu email bizda mavjud emas')

            code = random.randint(1000, 9999)
            VerifyCodes.objects.create(
                user=user,
                code=code
            )

            data = {
                'status': status.HTTP_200_OK,
                'message': 'Kodingiz yuborildi'
            }
            return Response(data)

        data = {
            'status': status.HTTP_200_OK,
            'message': 'Kodingiz yuborildi'
        }

        return Response(data)


class ResetCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        if not email or not code:
            return Response({"detail": "email va code majburiy"}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"detail": "Bu email bilan user topilmadi"}, status=404)

        vc = VerifyCodes.objects.filter(user=user, code=code, is_active=False).first()
        if not vc:
            return Response({"detail": "Kod noto‘g‘ri yoki ishlatilgan"}, status=400)

        if vc.expiration_time < timezone.now():
            return Response({"detail": "Kod muddati tugagan"}, status=400)

        vc.is_active = True
        vc.save(update_fields=["is_active"])

        return Response({"detail": "Kod tasdiqlandi"}, status=200)

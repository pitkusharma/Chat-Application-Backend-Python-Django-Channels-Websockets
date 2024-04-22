from rest_framework import views, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import LoginSerializer, RefreshTokenSerializer
from .models import LoginData
from utilities.encryption import Encrypt
from .jwt_authentication import GenerateTokens, JWTAuthentication
from utilities.util import get_client_ip, get_user_agent
from rest_framework.permissions import AllowAny, IsAuthenticated


Users = get_user_model()

class Login(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serialized_data = LoginSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response({'message': f'Invalid data: {serialized_data.errors}'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = Users.objects.filter(username=serialized_data.validated_data.get('username')).first()
        if not user:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        encrypt = Encrypt(serialized_data.validated_data.get('password'), user.password)
        if not encrypt.compare_encrypted_values():
            return Response({'message': 'User credentials are wrong'}, status=status.HTTP_401_UNAUTHORIZED)
        jwt_auth = GenerateTokens(user)
        data = {
            'access_token': jwt_auth.access_token(),
            'refresh_token': jwt_auth.refresh_token()
        }
        login_record = LoginData.objects.create(user=user, username=user.username, ip_address=get_client_ip(request), user_agent=get_user_agent(request))
        return Response(data, status=status.HTTP_200_OK)

class RefreshToken(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serialized_data = RefreshTokenSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response({'message': f'Invalid data: {serialized_data.errors}'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        refresh_token = serialized_data.validated_data.get('refresh_token')
        try:
            user, token_data = JWTAuthentication.verify_token(refresh_token)
        except:
            return Response({'message': f'Invalid token: {serialized_data.errors}'}, status=status.HTTP_400_BAD_REQUEST)
        jwt_auth = GenerateTokens(user)
        data = {
            'access_token': jwt_auth.access_token(),
        }
        return Response(data, status=status.HTTP_200_OK)

class VerifyAccessToken(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'message': f'Authenticated'}, status=status.HTTP_200_OK)






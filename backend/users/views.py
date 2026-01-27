from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import (
    User,
    HospitalProfile,
    BloodBankProfile,
    AdminProfile,
)
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    HospitalProfileSerializer,
    BloodBankProfileSerializer,
    AdminProfileSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    API endpoint for user login
    """
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'detail': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    API endpoint for user registration
    """
    serializer = UserRegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    User ViewSet for CRUD operations
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'register']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Get current user info
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """
        Filter users by type
        """
        user_type = request.query_params.get('type')

        if user_type:
            users = User.objects.filter(user_type=user_type)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)

        return Response(
            {"error": "type parameter required"},
            status=status.HTTP_400_BAD_REQUEST
        )


class HospitalProfileViewSet(viewsets.ModelViewSet):
    """
    Hospital Profile ViewSet
    """
    queryset = HospitalProfile.objects.all()
    serializer_class = HospitalProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'hospital':
            return HospitalProfile.objects.filter(user=self.request.user)
        return HospitalProfile.objects.all()


class BloodBankProfileViewSet(viewsets.ModelViewSet):
    """
    Blood Bank Profile ViewSet
    """
    queryset = BloodBankProfile.objects.all()
    serializer_class = BloodBankProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'bloodbank':
            return BloodBankProfile.objects.filter(user=self.request.user)
        return BloodBankProfile.objects.all()


class AdminProfileViewSet(viewsets.ModelViewSet):
    """
    Admin Profile ViewSet
    """
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'admin':
            return AdminProfile.objects.filter(user=self.request.user)
        return AdminProfile.objects.all()





def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  
        else:
            return render(request, 'auth/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'users/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'auth/registration.html', {
                'error': 'Passwords do not match'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'auth/registration.html', {
                'error': 'Username already exists'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            user_type=user_type
        )

        login(request, user)
        return redirect('login')

    return render(request, 'users/registration.html')

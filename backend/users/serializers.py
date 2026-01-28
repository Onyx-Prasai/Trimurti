from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, HospitalProfile, BloodBankProfile, AdminProfile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 'is_verified', 'phone_number', 'location', 'profile_picture']
        read_only_fields = ['id', 'is_verified']


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'user_type', 'first_name', 'last_name', 'phone_number', 'location']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'location': {'required': False},
            # Registration in the app is donor-only; default to base_user if omitted
            'user_type': {'required': False},
        }
    
    def validate_password(self, value):
        """Validate password strength"""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': "Passwords don't match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        validated_data.setdefault('user_type', 'base_user')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class HospitalProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Hospital Profile
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = HospitalProfile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class BloodBankProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for BloodBank Profile
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = BloodBankProfile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AdminProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Admin Profile
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = AdminProfile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

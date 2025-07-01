from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# Signup serializer
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone_number', 'email', 'password',]  # Include gender first
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data.get('email')
        phone_number = data.get('phone_number')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'This email is already taken.'})
        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({'phone_number': 'This phone number is already taken.'})
        return data

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
              # Set gender during user creation
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Login serializer (JWT)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email and password:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                token = RefreshToken.for_user(user)
                return {
                    'user_id': str(user.user_id),  # Include user ID in the response
                    'email': user.email,
                    'refresh': str(token),
                    'access': str(token.access_token),
                    'name': user.name,  # Include name in the response
                }
            else:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Both email and password are required')

# Custom JWT serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims (e.g., user_id and name)
        token['user_id'] = str(user.user_id)  # Include user ID
        token['name'] = user.name  # Include name
        return token

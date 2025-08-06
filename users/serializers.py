# users/serializers.py
from rest_framework import serializers
from .models import CustomUser, Artist, Investor
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from posts.serializers import PostSerializer 
from cloudinary.models import CloudinaryField

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_or_email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None) 
    
    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')

        if not username_or_email:
            raise serializers.ValidationError({"detail": "Username or email is required."})
        if not password:
            raise serializers.ValidationError({"detail": "Password is required."})

        user = None
        if '@' in username_or_email: 
            try:
                temp_user = CustomUser.objects.get(email__iexact=username_or_email)
                if temp_user.check_password(password):
                    user = temp_user
            except CustomUser.DoesNotExist:
                pass
        
        if not user:
            try:
                temp_user = CustomUser.objects.get(username__iexact=username_or_email)
                if temp_user.check_password(password): 
                    user = temp_user
            except CustomUser.DoesNotExist:
                pass 
        if not user or not user.is_active:
            raise serializers.ValidationError({"detail": "No active account found with the given credentials."})

        attrs['username'] = user.username
        attrs['password'] = password 
        data = super().validate(attrs)
        data['user_type'] = user.user_type
        
        return data

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, required=True)
    profile_picture = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'full_name', 'email', 'phone_number', 'country',
            'date_of_birth', 'profile_picture', 'user_type', 'password', 'confirm_password' 
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
            'age': {'read_only': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "كلمة السر وتأكيدها غير متطابقين."})
        
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "هذا البريد الإلكتروني مسجل بالفعل."})
        if CustomUser.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError({"phone_number": "رقم الهاتف هذا مسجل بالفعل."})
        
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password') 
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            country=validated_data['country'],
            date_of_birth=validated_data['date_of_birth'],
            profile_picture=validated_data.get('profile_picture'),
            user_type=validated_data['user_type'] 
        )
        return user 

class ArtistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['art_section', 'artistic_bio', 'artistic_achievements', 'what_i_need']

class InvestorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ['support_type', 'own_art_company', 'company_name', 'company_art_field', 'art_section', 'what_i_need', 'bio']
        extra_kwargs = {
            'company_name': {'required': False},
            'company_art_field': {'required': False},
        }

    def validate(self, data):
        if data.get('own_art_company') and not data.get('company_name'):
            raise serializers.ValidationError({"company_name": "Company name is required if you own a company."})
        if data.get('own_art_company') and not data.get('company_art_field'):
            raise serializers.ValidationError({"company_art_field": "Company art field is required if you own a company."})
        return data

class ArtistRegistrationSerializer(CustomUserSerializer):
    artist_profile = ArtistProfileSerializer()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + ['artist_profile']

    def create(self, validated_data):
        artist_profile_data = validated_data.pop('artist_profile')
        validated_data['user_type'] = "ARTIST" 
        user = super().create(validated_data)
        Artist.objects.create(user=user, **artist_profile_data)
        return user

class InvestorRegistrationSerializer(CustomUserSerializer):
    investor_profile = InvestorProfileSerializer()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + ['investor_profile']

    def create(self, validated_data):
        investor_profile_data = validated_data.pop('investor_profile')
        validated_data['user_type'] = "INVESTOR" 
        user = super().create(validated_data)
        Investor.objects.create(user=user, **investor_profile_data)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True) 
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "كلمة السر وتأكيدها غير متطابقين."})
        
        try:
            self.user = CustomUser.objects.get(email__iexact=data['email'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"email": "لا يوجد مستخدم مسجل بهذا البريد الإلكتروني."})
        
        return data

    def save(self, **kwargs):
        self.user.set_password(self.validated_data['password'])
        self.user.save() 
        return self.user

class UserProfileDetailSerializer(serializers.ModelSerializer):
    artist_profile = ArtistProfileSerializer(read_only=True)
    investor_profile = InvestorProfileSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'full_name', 'email', 'phone_number', 'country',
            'date_of_birth', 'age', 'profile_picture', 'user_type', 
            'artist_profile', 'investor_profile','posts'
        ]
        read_only_fields = [ 'age', 'user_type', 'posts'] 
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'confirm_password': {'write_only': True, 'required': False},
        }
    
    def validate(self, data):
     
        if 'email' in data:
            if CustomUser.objects.filter(email=data['email']).exists() and self.instance.email != data['email']:
                raise serializers.ValidationError({"email": "هذا البريد الإلكتروني مسجل بالفعل."})
        
        if 'phone_number' in data:
            if CustomUser.objects.filter(phone_number=data['phone_number']).exists() and self.instance.phone_number != data['phone_number']:
                raise serializers.ValidationError({"phone_number": "رقم الهاتف هذا مسجل بالفعل."})
            
        if 'username' in data:
            new_username = data['username']
            if CustomUser.objects.filter(username__iexact=new_username).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({"username": "اسم المستخدم هذا مستخدم بالفعل."})
        
        return data

    def update(self, instance, validated_data):
        validated_data.pop('user_type', None)
        instance = super().update(instance, validated_data)

        if hasattr(instance, 'artist_profile'):
            artist_profile_data = validated_data.pop('artist_profile', {})
            artist_serializer = ArtistProfileSerializer(instance.artist_profile, data=artist_profile_data, partial=True)
            if artist_serializer.is_valid(raise_exception=True):
                artist_serializer.save()
        elif hasattr(instance, 'investor_profile'):
            investor_profile_data = validated_data.pop('investor_profile', {})
            investor_serializer = InvestorProfileSerializer(instance.investor_profile, data=investor_profile_data, partial=True)
            if investor_serializer.is_valid(raise_exception=True):
                investor_serializer.save()
        return instance

class UserSearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'profile_picture', 'user_type', 'country']
        read_only_fields = [ 'full_name', 'profile_picture', 'user_type', 'country']
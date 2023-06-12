from django.db.models import Q

from rest_framework import serializers

from accounts.models import *

class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        
    def validate(self,data):
        errors = []
        if not self.partial:
            required_keys = ['email','first_name']
            for key in required_keys:
                if not data.get(key):
                    errors.append({key:"This field is requried"})
            
            if data.get('user_type','personal') == 'hr' and not data.get('company'):
                errors.append({"company":"This field is required for hr type users"})
            
        phone = data.get('phone')
        email = data.get('email')
        password = data.get('password')
        
        if phone and len(phone) != 10:
            errors.append({"phone":"This field must have 10 digits"})
        
        if email and Account.objects.filter(email=email).exists():
            errors.append({"email":"User with this email is already exists"})
        
        if phone and Account.objects.filter(phone=phone).exists():
            errors.append({"phone":"User with this phone is already exists"})
        
        if password and len(password) < 8:
            errors.append({"password":"Password must contains atleast 8 characters"})
        
        if errors:
            raise serializers.ValidationError({"errors":errors})
        return data


class ViewAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['password','groups']
    

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        
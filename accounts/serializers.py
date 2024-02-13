from rest_framework import serializers
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'gender']


# registration serializer
class RegistrationSerializer(serializers.ModelSerializer):
  password2 = serializers.CharField(style={"input_type": 'password'}, write_only=True)
  class Meta:
    model = CustomUser
    fields = ['email', 'first_name', 'last_name','gender', 'password', 'password2', 'otp']
    extra_kwargs = {
        'password': {'write_only': True}
    }

  def save(self):
    email = self.validated_data['email']
    first_name = self.validated_data['first_name']
    last_name = self.validated_data['last_name']
    gender = self.validated_data['gender']
    password = self.validated_data['password']
    otp = self.validated_data['otp']
    password2 = self.validated_data['password2']
    user = CustomUser(email=email, first_name=first_name, last_name=last_name, gender=gender, otp=otp)

    if password != password2:
      raise serializers.ValidationError({'password': 'Passwords must match.'})
    user.set_password(password)
    user.save()
    return user

# class RegistrationSerializer(serializers.ModelSerializer):
#   password2 = serializers.CharField(style={"input_type": 'password'}, write_only=True)
#   class Meta:
#     model = CustomUser
#     fields = ['email', 'otp', 'first_name', 'last_name', 'phone', 'gender', 'password', 'password2']
#     extra_kwargs = {
#         'password': {'write_only': True}
#     }

#   def save(self):

#     email = self.validated_data['email']
#     first_name = self.validated_data['first_name']
#     last_name = self.validated_data['last_name']
#     phone = self.validated_data['phone']
#     otp = self.validated_data['otp']
#     gender = self.validated_data['gender']
#     password = self.validated_data['password']
#     password2 = self.validated_data['password2']
#     user = CustomUser(email=email, first_name=first_name, last_name=last_name, phone=phone, otp=otp, gender=gender)

#     if password != password2:
#       raise serializers.ValidationError({'password': 'Passwords must match.'})
#     user.set_password(password)
#     user.save()
#     return user

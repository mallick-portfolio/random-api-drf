from rest_framework import serializers
from accounts.models import CustomUser

class RegistrationSerializer(serializers.ModelSerializer):
  password2 = serializers.CharField(style={"input_type": 'password'}, write_only=True)
  class Meta:
    model = CustomUser
    fields = ['email', 'username', 'first_name', 'last_name', 'phone', 'date_of_birth', 'password', 'password2']
    extra_kwargs = {
        'password': {'write_only': True}
    }

  def save(self):

    email = self.validated_data['email']
    username = self.validated_data['username']
    first_name = self.validated_data['first_name']
    last_name = self.validated_data['last_name']
    phone = self.validated_data['phone']
    date_of_birth = self.validated_data['date_of_birth']
    password = self.validated_data['password']
    password2 = self.validated_data['password2']
    user = CustomUser(email=email, username=username, first_name=first_name, last_name=last_name, phone=phone, date_of_birth = date_of_birth)

    if password != password2:
      raise serializers.ValidationError({'password': 'Passwords must match.'})
    user.set_password(password)
    user.save()
    return user

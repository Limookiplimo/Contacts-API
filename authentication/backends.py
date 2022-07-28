from django.conf import settings
import jwt
from rest_framework import authentication, exceptions
from django.contrib.auth.models import User

class JWTAuthentication(authentication.BasicAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None
        
        prefix, token = auth_data.decode('utf-8').split(' ')

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])

            user = User.objects.get(id=payload['id'])
            return (user, token)


        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid token')
        
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Expired token')
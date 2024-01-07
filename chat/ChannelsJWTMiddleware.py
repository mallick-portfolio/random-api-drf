from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):

        query_string = scope.get('query_string').decode()
        if not query_string:
            scope['user'] = None
            return 
        token = query_string.split('=')[1]

        try:
            user = AccessToken(token).payload
            scope['user'] = user['user_id']
        except:
            scope['user'] = None
        return await self.inner(scope, receive, send)



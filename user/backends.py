from django.contrib.auth.backends import ModelBackend
from .models import User

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print("backends", self, request.user)
        try:
            user = User.objects.get(email=email)
        except Exception:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
# authentication/authentication.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username, password, **kwargs):
        UserModel = get_user_model()

        # Check if the provided username is an email address
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}

        # Use Q object to query with OR condition
        try:
            user = UserModel.objects.get(Q(**kwargs))
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

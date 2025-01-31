from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

class DebugAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            logger.info(f"Found user: {username}")
            
            if user.check_password(password):
                logger.info(f"Password check passed for user: {username}")
                return user
            else:
                logger.warning(f"Password check failed for user: {username}")
                return None
        except UserModel.DoesNotExist:
            logger.warning(f"User does not exist: {username}")
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

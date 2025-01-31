from django.core.exceptions import ValidationError
import re

class CustomPasswordValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                f'Password must be at least {self.min_length} characters long.',
                code='password_too_short',
            )
        
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                'Password must contain at least one lowercase letter.',
                code='password_no_lower',
            )
            
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                'Password must contain at least one uppercase letter.',
                code='password_no_upper',
            )

    def get_help_text(self):
        return f'Your password must be at least {self.min_length} characters long and contain at least one lowercase and one uppercase letter.'

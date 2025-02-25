# users/utils.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_verified)
        )

email_verification_token = EmailVerificationTokenGenerator()

class ResetPasswordTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )

reset_password_token = ResetPasswordTokenGenerator()

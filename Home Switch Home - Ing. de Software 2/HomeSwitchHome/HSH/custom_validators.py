from django.utils.translation import ngettext  # https://docs.python.org/2/library/gettext.html#gettext.ngettext
from django.core.exceptions import ValidationError

# https://docs.djangoproject.com/en/2.0/_modules/django/contrib/auth/password_validation/#MinimumLengthValidator
class MyCustomMinimumLengthValidator(object):
    def __init__(self, min_length=8):  # put default min_length here
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    # silly, I know, but if your min length is one, put your message here
                    "Esta contraseña es muy corta. Debe contener al menos %(min_length)d caracteres.",
                    # if it's more than one (which it probably is) put your message here
                    "Esta contraseña es muy corta. Debe contener al menos %(min_length)d caracteres.",
                    self.min_length
                ),
            code='password_too_short',
            params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            # you can also change the help text to whatever you want for use in the templates (password.help_text)
            "Tu contraseña debe contener al menos %(min_length)d caracteres.",
            "Tu contraseña debe contener al menos %(min_length)d caracteres.",
            self.min_length
        ) % {'min_length': self.min_length}


class MyCustomNumericPasswordValidator(object):

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                ("Esta contraseña está compuesta solo por números."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("Tu contraseña no puede contener solo números.")
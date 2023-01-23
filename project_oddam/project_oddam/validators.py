import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _("Twoje hasło musi zawierać przynajmniej jedną cyfrę od 0-9."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Twoje hasło musi zawierać przynajmniej jedną cyfrę od 0-9."
        )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("Twoje hasło musi zawierać przynajmniej jedną wielką literę."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Twoje hasło musi zawierać przynajmniej jedną wielką literę."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("Twoje hasło musi zawierać przynajmniej jeden znak specjalny: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Twoje hasło musi zawierać przynajmniej jeden znak specjalny: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )
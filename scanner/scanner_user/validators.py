from django.core.exceptions import ValidationError


def validate_email_domain(value):
    """ Валидация почтовых адресов. """
    valid_domain_endings = ['.ru', '.su', '.рф']
    email_parts = value.split('@')
    if len(email_parts) == 2:
        domain = email_parts[1].lower()
        if not any(domain.endswith(ending) for ending in valid_domain_endings):
            raise ValidationError('Допустимые домены почты: ru, su, рф')

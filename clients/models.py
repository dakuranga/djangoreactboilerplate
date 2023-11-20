from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.validators import FileExtensionValidator

def add_http_prefix(value):
    if not value.startswith(('http://', 'https://')):
        return f'http://{value}'
    return value

def add_http_prefix_and_validate_url(value):
    value = add_http_prefix(value)
    URLValidator()(value)
    return value

class URLFieldWithPrefix(models.CharField):
    default_validators = [add_http_prefix_and_validate_url]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 200
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        value = add_http_prefix(value)
        setattr(model_instance, self.attname, value)
        return value

def validate_pdf_extension(value):
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')

class Client(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    website = URLFieldWithPrefix(unique=True)
    industry = models.CharField(max_length=200)
    hq = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    about_client_attachment = models.FileField(upload_to='About_clients/',validators=[FileExtensionValidator(allowed_extensions=['pdf']), validate_pdf_extension], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

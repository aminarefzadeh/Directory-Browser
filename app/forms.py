from django.forms import ModelForm
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        exclude=['groups','user_permissions','is_staff','is_active','date_joined','is_superuser','last_login']
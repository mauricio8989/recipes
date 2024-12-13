from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'password',
                  'password_repeat']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password_repeat'], 'Repeat your password')

    first_name = forms.CharField(
        error_messages={
            'required': 'Write your first name here',
        },
        label='First name'
    )
    last_name = forms.CharField(
        error_messages={
            'required': 'Write your last name here',
        },
        label='Last name'
    )
    username = forms.CharField(
        help_text={
            'max_length': 'Username should be between 4 and 150 characters',
        },
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less 150 characters',
            'unique': 'This username already exists',
        },
        label='Username',
        max_length=150,
        min_length=4,

    )
    email = forms.EmailField(
        error_messages={
            'required': 'Invalid email address',
            'unique': 'This email address already exists.',
        },
        label='E-mail',
    )
    password = forms.CharField(
        error_messages={
            'required': 'Password must not be empty',
        },
        label='Password',
        validators=[strong_password],
        widget=forms.PasswordInput,
    )
    password_repeat = forms.CharField(
        error_messages={
            'required': 'Please, repeat your pasword here',
        },
        label='Password_repear',
        widget=forms.PasswordInput,
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError(
                'This email address already exists.', code='invalid')
        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')

        if password != password_repeat:
            password_confirmation_error = forms.ValidationError(
                'Password and password_repeat must be equal',
                code='invalid'
            )
            raise forms.ValidationError({
                'password': password_confirmation_error,
                'password_repeat': [
                    password_confirmation_error,
                ],
            })


class LogInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

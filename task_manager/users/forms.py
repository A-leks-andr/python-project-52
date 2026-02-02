from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators


class UserRegistrationForm(UserCreationForm):
    MIN_LENGTH_VALIDATOR = validators.MinLengthValidator(3)

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"minlength": "3", "autocomplete": "new-password"}
        ),
        strip=False,
        help_text="Ваш пароль должен содержать минимум 3 символа.",
        validators=[MIN_LENGTH_VALIDATOR],
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={"minlength": "3", "autocomplete": "new-password"}
        ),
        strip=False,
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз.",
        validators=[MIN_LENGTH_VALIDATOR],
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]
        widgets = {
            "username": forms.TextInput(attrs={"autocomplete": "off"}),
        }


class UserUpdateDataForm(forms.ModelForm):
    MIN_LENGTH_VALIDATOR = validators.MinLengthValidator(3)

    password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "minlength": "3"}
        ),
        required=True,
        help_text="Оставьте пустым, если не хотите менять пароль.",
        validators=[MIN_LENGTH_VALIDATOR],
    )
    password2 = forms.CharField(
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "minlength": "3"}
        ),
        required=True,
        help_text="Введите новый пароль еще раз.",
        validators=[MIN_LENGTH_VALIDATOR],
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"autocomplete": "off"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        # Если заполнен только один из паролей
        if (password1 and not password2) or (not password1 and password2):
            raise forms.ValidationError(
                "Для смены пароля необходимо заполнить оба поля."
            )

        return cleaned_data

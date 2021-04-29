from django.forms import ModelForm
from MainApp.models import Snippet
from django.contrib.auth.models import User
from django import forms


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        widgets = {
            'name': forms.TextInput(attrs={'class': 'none'})
        }
        # Описываем поля, которые будем заполнять в форме
        fields = ['name', 'lang', 'code', 'public']


class UserRegisterForm(forms.ModelForm):
    # Упрощенная форма регистрации на основе UserCreationForm:
    # https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/
    # Подробно работа с формами тут: https://djbook.ru/rel1.8/ref/forms/api.html#module-django.forms
    class Meta:
        model = User
        fields = ("username", "email")

    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
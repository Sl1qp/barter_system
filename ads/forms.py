from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Ad, Category, Condition, ExchangeProposal


class AdForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категория",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    condition = forms.ModelChoiceField(
        queryset=Condition.objects.all(),
        label="Состояние",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Ad
        fields = ["title", "description", "image_url", "category", "condition"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "image_url": forms.URLInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Заголовок",
            "description": "Описание",
            "image_url": "Ссылка на изображение (необязательно)",
        }

    def clean_image_url(self):
        url = self.cleaned_data.get("image_url")
        if url and not url.startswith(("http://", "https://")):
            raise forms.ValidationError("Некорректный URL. Используйте http:// или https://.")
        return url


class ExchangeProposalForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["ad_sender"].queryset = Ad.objects.filter(user=user)
        self.fields["ad_receiver"].queryset = Ad.objects.exclude(
            user=user)

    class Meta:
        model = ExchangeProposal
        fields = ["ad_sender", "ad_receiver", "comment"]
        labels = {
            "ad_sender": "Ваше объявление",
            "ad_receiver": "Предложенный обмен",
            "comment": "Комментарий",
        }
        widgets = {
            "ad_sender": forms.Select(attrs={"class": "form-control"}),
            "ad_receiver": forms.Select(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class ProposalStatusForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "status": "Изменить статус",
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text", "group")
        labels = {
            "text": _("Текст поста"),
            "group": _("Группа")
        }
        help_texts = {
            "text": _("Текст поста"),
            "group": _("Группа, к которой относится пост")
        }
        widgets = {
            "group": forms.Select(attrs={"class": "custom-select md-form"}),
        }
        error_messages = {
            "text": {
                'null': 'Пожалуйста, введите текст'
            },
        }

from django import forms
from django.utils.html import escape


class XSSForm(forms.Form):
    """
    Форма для защищённого режима (secure)

    Здесь мы:
    1. Валидируем входные данные
    2. Экранируем потенциально опасный HTML (XSS)
    """

    query = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "Введите текст..."}),
    )

    def clean_query(self):
        """
        Очистка данных от XSS
        """
        data = self.cleaned_data.get("query", "")
        # Экранируем HTML-теги
        # <script> → &lt;script&gt;
        safe_data = escape(data)
        return safe_data


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    def clean_text(self):
        return escape(self.cleaned_data["text"])

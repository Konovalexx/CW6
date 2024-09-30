from django import forms
from catalog.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'content', 'preview', 'category', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        if any(word in title.lower() for word in forbidden_words):
            raise forms.ValidationError("Название статьи содержит запрещенные слова.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        if any(word in content.lower() for word in forbidden_words):
            raise forms.ValidationError("Текст статьи содержит запрещенные слова.")
        return content
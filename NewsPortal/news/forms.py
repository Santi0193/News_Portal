from django import forms
from .models import News, Post, Category

class NewsSearchForm(forms.Form):
    title = forms.CharField(required=False, label='Поиск по названию')
    author = forms.CharField(required=False, label='Поиск по автору')
    created_at = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))

class NewsForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = News
        fields = ['title', 'text', 'author']

class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'type', 'categories']
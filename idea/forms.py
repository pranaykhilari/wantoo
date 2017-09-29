from django import forms
from django.forms import ModelForm
from .models import Idea, Comment, Category, Status


class IdeaForm(ModelForm):
    def __init__(self, company, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        self.fields['title'] = forms.CharField(widget=forms.TextInput(attrs={'maxlength':70}))
        self.fields['description'] = forms.CharField(required=False, widget=forms.Textarea(attrs={'maxlength':5000}))
        self.fields['description'].label = 'Description'
        if self.instance:
            self.fields['category'].queryset = Category.objects.filter(company=company)
            self.fields['status'].queryset = Status.objects.filter(company=company)

    class Meta:
        model = Idea
        fields = ['title','description','category', 'status']        


class CategoryForm(ModelForm):
    def __init__(self, company, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Category
        exclude = ['created_by','created_at','company']        


class StatusForm(ModelForm):
    def __init__(self, company, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        self.fields['color'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'jscolor'}))
        self.fields['color'].initial = "66961a"
        self.fields['color'].label = "Status color"
        self.fields['color'].help_text = "Use a hex color for this status. ie. EEEEEE"
    class Meta:
        model = Status
        exclude = ['created_by','created_at','company']        


class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ['comment',]                
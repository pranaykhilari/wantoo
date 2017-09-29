from django import forms
from django.forms import ModelForm
from .models import Company, Member, UserDetail
from allauth.account.forms import LoginForm

class CompanyAddForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CompanyAddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Company
        fields = ['title',]       


class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['color'] = forms.CharField(required=False,
                                               widget=forms.TextInput(attrs={'class': 'jscolor text_field input_font'}))
        self.fields['logo_url'] = forms.CharField(required=False,
                                               widget=forms.TextInput(attrs={'class': 'field_text input_font'}))
        self.fields['title'].widget.attrs['class'] = 'text_field input_font'
        self.fields['question'].widget.attrs['class'] = 'field_text input_font'

        self.fields['color'].label = "Theme color"
        self.fields['color'].help_text = "Use a 6-digit HEX or select from the color picker."

        self.fields['question'].help_text = "This will show up on your idea board's homepage and idea list views."

        self.fields['title'].label = "Title"
        self.fields['title'].help_text = "This will show up on notification emails."


    class Meta:
        model = Company
        fields = ['title', 'question', 'logo_url', 'color']                


class NotificationsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NotificationsForm, self).__init__(*args, **kwargs)
        self.fields['email_comment'].label = "Email me when someone comments on my idea"
        self.fields['email_want'].label = "Email me when someone wants my idea"
        self.fields['email_comment_on_want'].label = "Email me when comments are added to an idea I've wanted"
        self.fields['email_comment_on_comment'].label = "Email me when comments are added to an idea I've commented on"
        self.fields['email_digest'].label = "Email me weekly summary of updates"

    class Meta:
        model = UserDetail
        fields = ['email_comment', 'email_want', 'email_comment_on_want', 'email_comment_on_comment', 'email_digest']


class NewLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(NewLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['login'].widget.attrs['placeholder'] = "Email"

        # You don't want the `remember` field?
        if 'remember' in self.fields.keys():
            del self.fields['remember']

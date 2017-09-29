from django import forms
from django.forms import ModelForm
from users.models import FeatureCompany

class AddFeatureBoardForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddFeatureBoardForm, self).__init__(*args, **kwargs)
        self.fields['company'].help_text = "This is the default company. It's information will be used if you leave something blank"
        self.fields['title'].help_text = "Override the board title."
        self.fields['question'].help_text = "Override the board question."
        self.fields['url'].help_text = "The link that will open when users click on the item."

    class Meta:
        model = FeatureCompany
        fields = ['company', 'title', 'question', 'url']                

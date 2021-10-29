from django import forms


class NameForm(forms.Form):
    url_search = forms.CharField(label='URL', max_length=400)
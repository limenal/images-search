from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(max_length=50)
    count = forms.TypedChoiceField(choices=[(i, str(i)) for i in range(1, 11)], coerce=int)
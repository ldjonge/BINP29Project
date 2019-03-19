from django import forms

class SearchForm(forms.Form):
    nameSearch = forms.CharField(label="Taxon Name", max_length = 100, required=False)
    idSearch = forms.IntegerField(label="Taxon ID", required=False)

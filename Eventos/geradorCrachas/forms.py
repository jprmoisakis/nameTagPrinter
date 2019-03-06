from django import forms

class MyForm(forms.Form):
    tabelaCracha = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
    logoInput = forms.forms.FileField(required =True)    
    textoCracha = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 30}))

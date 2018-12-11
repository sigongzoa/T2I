from django import forms
from mylunch import choices as ch

class Filter_form(forms.Form):
    type = forms.DecimalField(label="type", max_digits=1, decimal_places=0,widget=forms.Select(choices=ch.TYPE, attrs={'style': 'width:200px'}),required=False,initial=0)
    price = forms.DecimalField(label="price", max_digits=1, decimal_places=0, widget=forms.Select(choices=ch.PRICE, attrs={'style': 'width:200px'}), required=False, initial=0)
    exp = forms.DecimalField(label="exp", max_digits=1, decimal_places=0, widget=forms.Select(choices=ch.EXP, attrs={'style': 'width:200px'}), required=False, initial=0)
    distance = forms.DecimalField(label="distance", max_digits=1, decimal_places=0, widget=forms.Select(choices=ch.DISTANCE, attrs={'style': 'width:200px'}), required=False, initial=0)


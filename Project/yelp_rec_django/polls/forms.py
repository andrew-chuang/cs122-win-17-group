# CS 122 Win' 17 
# Arif-Chuang-Hori-Teehan
#
#

from django import forms

class YelpForm(forms.Form):
    rest1 = forms.CharField(label='Restaurant 1', max_length=100)
    rest1_loc = forms.CharField(label='Location', max_length=100)
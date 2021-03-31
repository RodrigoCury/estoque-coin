from django import forms
from .models import Brand, Yeast, FermentativeProfile, Todo


class DateInput(forms.DateInput):
    input_type = 'date'


class YeastCreateForm(forms.ModelForm):
    class Meta:
        model = Yeast
        exclude = ['slug', 'user', 'next_reinnoculation_limit_date', ]
        widgets = {'created_at': DateInput(),
                   'last_reinnoculation': DateInput(),
                   }


class BrandCreateForm(forms.ModelForm):
    class Meta:
        model = Brand
        exclude = ['slug', ]


class FermentativeProfileCreateForm(forms.ModelForm):
    class Meta:
        model = FermentativeProfile
        exclude = ['slug', ]


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        exclude = ['complete', 'user']

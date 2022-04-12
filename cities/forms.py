from django.forms import (
    Form, ModelForm, CharField, TextInput,
)

from cities.models import City


class CityForm(Form):
    name = CharField(label='Город', widget=TextInput(attrs={'class': ' form-control',
                                                            'placeholder': 'введите название города', }))


class CityModelForm(ModelForm):
    class Meta:
        model = City
        fields = ('name',)
        widgets = {
            'name': TextInput(attrs={'class': ' form-control',
                                     'placeholder': 'введите название города', }),
        }

from datetime import datetime

from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import (
    Form, ModelForm, TextInput, Select,
    DateTimeInput, NumberInput, ModelChoiceField,
)

from trains.models import Train
from cities.models import City

queryset = City.objects.all()


class TrainModelForm(ModelForm):
    # from_city = ModelChoiceField(
    #     queryset=queryset, label=_('Из города'), widget=Select(
    #         attrs={'class': ' form-control', }
    #     )
    # )
    # to_city = ModelChoiceField(
    #     queryset=queryset, label=_('В город'), widget=Select(
    #         attrs={'class': ' form-control', }
    #     )
    # )
    departure_time = forms.DateTimeField(
        initial=datetime.now(),
        label='Время прибытия',
        widget=DateTimeInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    arrival_time = forms.DateTimeField(
        initial=datetime.now(),
        label='Время отбытия',
        widget=DateTimeInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Train
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'введите номер поезда',
                }
            ),
            'travel_time': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'время в пути',
                }
            ),
            'from_city': Select(
                attrs={
                    'class': 'form-control js-example-basic-single',
                }
            ),
            'to_city': Select(
                attrs={
                    'class': 'form-control js-example-basic-single',
                }
            ),
        }
        labels = {
            'name': _('Номер поезда'),
            'travel_time': _('Время путешествия в часах'),
            'from_city': _('Из города'),
            'to_city': _('В город'),
        }

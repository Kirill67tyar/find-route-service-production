from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import (
    Form, ModelForm, TextInput, HiddenInput, Select, SelectMultiple,
    DateTimeInput, NumberInput, ModelChoiceField, ModelMultipleChoiceField, CharField,
)

from cities.models import City
from routes.models import Route
from trains.models import Train

cities = City.objects.all()


class RouteForm(Form):
    from_city = ModelChoiceField(
        queryset=cities,
        label=_('Из города'),
        widget=Select(
            attrs={'class': ' form-control js-example-basic-single', }
        )
    )
    to_city = ModelChoiceField(
        queryset=cities,
        label=_('В город'),
        widget=Select(
            attrs={'class': 'form-control js-example-basic-single', }
        )
    )
    cities = ModelMultipleChoiceField(
        queryset=cities,
        label=_('Через какие города'),
        required=False,
        widget=SelectMultiple(
            attrs={'class': 'form-control js-example-basic-multiple', }
        )
    )
    traveling_time = forms.IntegerField(
        label=_('Ожидаемое время поездки'),
        widget=NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'время в пути', }
        ),
    )


class RouteModelForm(ModelForm):
    name = CharField(
        label='Название маршрута',
        widget=TextInput(attrs={
            'class': ' form-control',
            'placeholder': 'введите название маршрута',
        }
        )
    )

    # from_city = ModelChoiceField(
    #     queryset=cities,
    #     widget=HiddenInput()
    # )
    #
    # to_city = ModelChoiceField(
    #     queryset=cities,
    #     widget=HiddenInput()
    # )

    trains = ModelMultipleChoiceField(
        queryset=Train.objects.all(),
        required=False,
        widget=SelectMultiple(attrs={
            'class': 'form-control d-none',
        }
        )
    )

    class Meta:
        model = Route
        fields = '__all__'
        widgets = {
            'from_city': HiddenInput(),
            'to_city': HiddenInput(),
            # 'trains': SelectMultiple(
            #     attrs={'class': 'form-control d-none', }
            # ),
            'travel_times': HiddenInput(),
        }

from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import (
    Model, CharField, ForeignKey, PositiveSmallIntegerField, DateTimeField, CASCADE,
)

from cities.models import City


class Train(Model):
    name = CharField(
        max_length=50, unique=True, verbose_name='Название поезда'
    )
    travel_time = PositiveSmallIntegerField(verbose_name='Время в пути')
    from_city = ForeignKey(
        to='cities.City',
        on_delete=CASCADE,
        related_name='trains_start',
        verbose_name='Из какого города'
    )
    to_city = ForeignKey(
        to='cities.City',
        on_delete=CASCADE,
        related_name='trains_arrive',
        verbose_name='В какой город'
    )
    departure_time = DateTimeField(verbose_name='Время отправления')
    arrival_time = DateTimeField(verbose_name='Время прибытия')

    def __str__(self):
        return f'Поезд № {self.name}, {self.from_city} - {self.to_city}'

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        unique_together = (
            'travel_time', 'from_city', 'to_city',
        )
        ordering = ('travel_time',)

    # Вообще этот метод clean() есть и в обычных формах.
    # И в формах он занимается также вопросом валидации (причем там он автоматически вызывается
    # после проверки is_valid(), тк там можно использовать cleaned_data())
    # Но здесь мы будем его вызывать в модельном методе save()
    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('Город отправления/прибытия должен быть изменен')

        # # Ниже пример неудачного кода как по мне. Проще определить атрибут unique_together в классе Meta
        # # что я и сделал. Более того, не всегда django использует метод save при сохранении в бд,
        # # при update метод save вроде как не используется
        # qs = self.__class__.objects.filter(from_city=self.from_city,
        #                           to_city=self.to_city,
        #                           travel_time=self.travel_time).exclude(pk=self.pk)
        # if qs.exists():
        #     raise ValidationError('Ошибка. Такой поезд уже есть')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy(
            'trains:detail', kwargs={'pk': self.pk, }
        )

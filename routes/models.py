from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.db.models import (
    Model, CharField, ForeignKey, ManyToManyField,
    PositiveSmallIntegerField, DateTimeField, CASCADE,
)

from cities.models import City


class Route(Model):
    name = CharField(
        max_length=50, unique=True, verbose_name='Название маршрута'
    )
    travel_times = PositiveSmallIntegerField(
        verbose_name='Общее время в пути'
    )
    from_city = ForeignKey(
        to='cities.City', on_delete=CASCADE,
        related_name='routes_start', verbose_name='Из какого города'
    )
    to_city = ForeignKey(
        to='cities.City', on_delete=CASCADE,
        related_name='routes_arrive', verbose_name='В какой город'
    )
    trains = ManyToManyField(
        to='trains.Train',
        related_name='routes',
        verbose_name='Список поездов'
    )

    def __str__(self):
        return f'Маршрут {self.name}, {self.from_city} - {self.to_city}'

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        # unique_together = ('travel_time', 'from_city', 'to_city',)
        ordering = ('travel_times',)

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('Маршрут отправления/прибытия должен быть изменен')

        # # Ниже пример неудачного кода как по мне. Проще определить атрибут unique_together в классе Meta
        # # что я и сделал. Более того, не всегда django использует метод save при сохранении в бд,
        # # при update метод save вроде как не используется
        # qs = self.__class__.objects.filter(from_city=self.from_city,
        #                           to_city=self.to_city,
        #                           travel_times=self.travel_times).exclude(pk=self.pk)
        # if qs.exists():
        #     raise ValidationError('Ошибка. Такой маршрут уже есть')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse_lazy(
    #         'routes:detail', kwargs={'pk': self.pk, }
    #     )

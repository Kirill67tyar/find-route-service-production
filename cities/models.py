from django.urls import reverse_lazy
from django.db.models import (Model, CharField, )


class City(Model):
    name = CharField(max_length=100, unique=True, verbose_name='Название города')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'города'
        verbose_name_plural = 'город'
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse_lazy('cities:detail', kwargs={'pk': self.pk, })

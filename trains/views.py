from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, )

from trains.models import Train
from trains.forms import TrainModelForm
from cities.utils import get_object_or_null, get_view_at_console1 as cons

__all__ = (
    'home_view', 'TrainListView',
    'TrainDetailView', 'TrainCreateView',
    'TrainUpdateView', 'TrainDeleteView',
)


def home_view(request):
    # trains = Train.objects.values()
    trains = Train.objects.all()
    paginator = Paginator(object_list=trains, per_page=5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'object_list': trains,
        'page_obj': page_obj,
    }

    return render(request, 'trains/home.html', context=context)


class TrainListView(ListView):
    model = Train
    paginate_by = 5
    template_name = 'trains/home.html'


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'

    def get(self, request, *args, **kwargs):
        cons(self.queryset)
        return super().get(request, *args, **kwargs)


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    # model = Train
    form_class = TrainModelForm
    template_name = 'trains/create.html'
    success_message = 'Поезд успешно создан'

    # success_url = reverse_lazy('trains:home')

    def get_success_url(self):
        url = reverse_lazy(
            'trains:detail', kwargs={'pk': self.object.pk}
        )
        return url


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Train
    form_class = TrainModelForm
    template_name = 'trains/update.html'
    success_message = 'Поезд успешно отредактирован'

    def get_success_url(self):
        url = reverse_lazy(
            'trains:detail', kwargs={'pk': self.object.pk}
        )
        return url


class TrainDeleteView(LoginRequiredMixin, DeleteView):
    model = Train
    success_url = reverse_lazy('trains:home')

    # template_name = 'trains/delete.html'

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Поезд успешно удалён')
        return self.post(request, *args, **kwargs)

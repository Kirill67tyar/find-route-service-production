from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.messages.views import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, DeleteView,
)

from routes.models import Route
from trains.models import Train
from cities.models import City
from routes.utils import get_routes
from routes.forms import RouteForm, RouteModelForm

__all__ = (
    'home_view', 'find_route_view',
    'add_route_view', 'save_route_view',
    'RouteListView', 'RouteDetailView',
    'RouteDeleteView',
)


def home_view(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form, })


def find_route_view(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as err:
                messages.error(request, err)
                return render(request, 'routes/home.html', {'form': form, })
            return render(request, 'routes/home.html', context)
        return render(request, 'routes/home.html', {'form': form, })
    else:
        return redirect(reverse('home'))


def add_route_view(request):
    if request.method == 'POST':
        data = request.POST
        context = {}
        if data:
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            total_time = int(data['total_time'])
            trains = data['trains'].split(',')
            trains_ids = [int(t) for t in trains if t.isdigit()]
            qs = Train.objects.filter(pk__in=trains_ids).select_related('from_city', 'to_city')
            cities = City.objects.filter(
                pk__in=[from_city_id, to_city_id, ]).in_bulk()
            form = RouteModelForm(
                initial={
                    'from_city': cities[from_city_id],
                    'to_city': cities[to_city_id],
                    'travel_times': total_time,
                    'trains': qs,
                }
            )
            context['form'] = form
        return render(request, 'routes/create.html', context=context)
    else:
        messages.error(request, 'Не будь таким хитрожопым')
        return redirect('/')


def save_route_view(request):
    if request.method == 'POST':
        form = RouteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request, message='Маршрут успешно сохранён')
            return redirect('/')
        message = 'Не удалось сохранить маршрут. Шанс что вы здесь окажитесь, был крайне маловероятен, и всё же вам удалось'
        messages.error(request, message=message)
        return render(request, 'routes/create.html', {'form': form, })
    else:
        messages.error(request, 'Не удалось сохранить маршрут')
        return redirect('/')


class RouteListView(ListView):
    model = Route
    template_name = 'routes/list.html'
    paginate_by = 5


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    template_name = 'routes/detail.html'


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request=request, message='Маршрут удалён')
        return self.post(request, *args, **kwargs)

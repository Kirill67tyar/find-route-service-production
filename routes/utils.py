from trains.models import Train


# эта функция больше не нужна
def sort_routes_by_time(routes) -> list:
    sorted_routes = []
    sorted_times = list(set([r['total_time'] for r in routes]))
    sorted_times.sort()
    for time in sorted_times:
        for route in routes:
            if route['total_time'] == time:
                sorted_routes.append(route)
    return sorted_routes  # [{k:v},{k:v},{k:v},]


def dfs_paths(graph, start, goal):
    stack = [(start, [start, ])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_, ]))


def get_graph2(qs) -> dict:
    graph = {}
    for train in qs:
        graph.setdefault(train.from_city_id, set())
        graph[train.from_city_id].add(train.to_city_id)
    return graph


# для Train.objects.values()
def get_graph(qs) -> dict:
    graph = {}
    for train in qs:
        graph.setdefault(train['from_city_id'], set())
        graph[train['from_city_id']].add(train['to_city_id'])
    return graph


def get_routes(request, form) -> dict:
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    traveling_time = data['traveling_time']
    cities = data['cities']
    # qs = Train.objects.values('id', 'name', 'travel_time', 'from_city_id', 'to_city_id',
    #                           'from_city__name', 'to_city__name')
    # qs = Train.objects.values()
    # мой вариант
    # graph = get_graph(qs=qs)

    # не мой вариант для all()
    # qs = Train.objects.all()
    qs = Train.objects.select_related('from_city', 'to_city').all()
    graph = get_graph2(qs=qs)

    # all_ways -- [[],[],]
    # к примеру если from_city.pk = 7, а to_city.pk = 10,
    # то результат как добраться от 7 до 10 будет такой:
    # [
    #   [7, 14, 18, 3, 10],
    #   [7, 14, 18, 3, 5, 10],
    #   [7, 3, 10],
    #   [7, 3, 5, 10],
    #   [7, 2, 14, 18, 3, 10],
    #   [7, 2, 14, 18, 3, 5, 10]
    # ]
    # тут видно, что напрямую поезд от города 7 до города 10 не ездит,
    # а проезжает через город 3
    all_ways = list(dfs_paths(
        graph=graph, start=from_city.pk, goal=to_city.pk
    ))
    if not len(all_ways):
        raise ValueError('Маршрут не найден')

    # проверяем, есть ли дополнительные города
    if cities:
        _cities = {city.pk for city in cities}
        right_ways = []

        # и есть ли эти города в хоть одном из маршрутов
        for route in all_ways:
            if all([city in route for city in _cities]):
                right_ways.append(route)
        if not right_ways:
            raise ValueError('Маршрут через эти города не возможен')
    # на тот случай, если дополнительных городов нет
    else:
        right_ways = all_ways

    # поиск маршрутов, которые подходят по времени
    routes_with_right_time = []
    all_trains = {}
    for train in qs:
        # all_trains -- {(from_city_id, to_city_id,): [{'id': 6, 'name': 't51', 'travel_time': 2, 'from_city_id': ...},]}
        # для values()
        # all_trains.setdefault((train['from_city_id'], train['to_city_id'],), [])
        # all_trains[(train['from_city_id'], train['to_city_id'],)].append(train)
        # для all()
        all_trains.setdefault((train.from_city_id, train.to_city_id,), [])
        all_trains[(train.from_city_id, train.to_city_id,)].append(train)
    for route in right_ways:
        tmp = {
            'trains': [],
        }
        total_time = 0
        # здесь находим время одного маршрута
        for i in range(len(route) - 1):
            # train -- {'id': 6, 'name': 't51', 'travel_time': 2, 'from_city_id': ...}
            train = all_trains[(route[i], route[i + 1])][0]
            # для value()
            # total_time += train['travel_time']
            # для all()
            total_time += train.travel_time
            tmp['trains'].append(train)
        tmp['total_time'] = total_time
        # если заданное пользователем время поездки больше или равно
        # времени одного полного маршрута, через все города, то добавляем в
        # переменную routes_with_right_time
        if total_time <= traveling_time:
            # routes_with_right_time -- [
            #                       { 'trains': [{'id': 6, 'name': 't51',...}, ...],
            #                       'total_time': n, },
            #                       { 'trains': ...}
            #                       ]
            routes_with_right_time.append(tmp)
    if not routes_with_right_time:
        raise ValueError('Нет маршрутов с подходящим временем')

    # сортировка маршрутов по времени (не важно, один он или много)
    routes_with_right_time.sort(key=lambda x: x['total_time'])
    sorted_routes = routes_with_right_time

    # # ---   ---   ---   ---   ---
    # # если бы я не отсортировал бы так :
    # # routes_with_right_time.sort(key=lambda x: x['total_time'])
    # # то пришлось бы делать последующую проверку,
    # # и использовать грамоздкую функцию наверху файла
    # if len(routes_with_right_time) == 1:
    #     # здесь нечего сортировать, т.к. маршрут всего один
    #     sorted_routes = routes_with_right_time
    # else:
    #     # здесь sorted_routes -- то же что и routes_with_right_time,
    #     # но отсортированная по времени
    #     sorted_routes = sort_routes_by_time(routes_with_right_time)
    # # ---   ---   ---   ---   ---


    #  сейчас этот участок кода не нужен,
    # он добавляет экземпляры City в values для Train
    # ids = [train['id'] for item in sorted_routes for train in item['trains'] ]
    # qs = Train.objects.filter(pk__in=ids)
    # for item in sorted_routes:
    #     for q in qs:
    #         pk = q.pk
    #         for train in item['trains']:
    #             if train['id'] == pk:
    #                 train['from_city'] = q.from_city
    #                 train['to_city'] = q.to_city
    # весь этот участок кода заменяет строка:
    # qs = Train.objects.values('id', 'name', 'travel_time', 'from_city_id', 'to_city_id',
    #                               'from_city__name', 'to_city__name')

    context = {
        'cities': {
            'from_city': from_city,  # модель города
            'to_city': to_city,  # модель города
        },
        'form': form,
        'routes': sorted_routes,
        # для values()
        # routes -- [
        #           { 'trains': [{'id': 6, 'name': 't51',...}, ...],
        #             'total_time': n, },
        #           { 'trains': ...}
        #           ]
    }
    return context

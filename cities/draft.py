"""
Можно попробовать эту иконку в качестве логотипа:
    <i class="fa fa-space-shuttle" aria-hidden="true"></i>

"""

from django.core.handlers.wsgi import WSGIRequest
from django.http.request import HttpRequest

# загрушка:


graph = None
from_city = None
to_city = None

# -----     -----     -----     -----     -----
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


all_ways = list(dfs_paths(
        graph=graph, start=from_city.pk, goal=to_city.pk
    ))




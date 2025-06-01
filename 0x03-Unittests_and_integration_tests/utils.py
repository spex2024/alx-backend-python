import requests
from functools import wraps

def access_nested_map(nested_map, path):
    """Access a nested map with a tuple path."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map

def get_json(url):
    """Get JSON data from a URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def memoize(method):
    """Memoization decorator for methods."""
    attr_name = "_memoized_" + method.__name__

    @property
    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)
    return wrapper
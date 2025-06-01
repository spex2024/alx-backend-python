import requests

def access_nested_map(nested_map, path):
    """Access a nested dictionary using a tuple path."""
    for key in path:
        if not isinstance(nested_map, dict):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


def get_json(url):
    """Get JSON from a URL using requests."""
    response = requests.get(url)
    return response.json()


def memoize(method):
    """Decorator to cache the result of a method call."""
    attr_name = f"_{method.__name__}"

    @property
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper

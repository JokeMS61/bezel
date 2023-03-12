__author__ = 'JK'

import datetime


class Cache:
    def __init__(self):
        self.cache = {}
        self.max_cache_size = 250

    def __contains__(self, key):
        # Returns True or False depending on whether or not the key is in the cache
        return key in self.cache

    def __getitem__(self, item):
        entry = self.cache[item]
        entry['date_accessed'] = datetime.datetime.now()
        surface = entry['value']
        return surface

    def __setitem__(self, key, item):
        self.cache[key] = item

    def update(self, key, value):
        # Update the cache dictionary and optionally remove the oldest item
        if key not in self.cache and len(self.cache) >= self.max_cache_size:
            self.remove_oldest()

        self.cache[key] = {'date_accessed': datetime.datetime.now(),
                           'value': value}

    def remove_oldest(self):
        # Remove the entry that has the oldest accessed date
        oldest_entry = None
        for key in self.cache:
            if oldest_entry is None:
                oldest_entry = key
            elif self.cache[key]['date_accessed'] < self.cache[oldest_entry]['date_accessed']:
                oldest_entry = key
        self.cache.pop(oldest_entry)

    @property
    def size(self):
        return len(self.cache)

    @property
    def maxsize(self):
        return self.max_cache_size


# -*- coding: utf-8 -*-
__author__ = 'Pig·Tong'

import functools


def get(path):
    """
        Define decorator @get('/path')
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper

    return decorator

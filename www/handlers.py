# -*- coding: utf-8 -*-
__author__ = 'Pig·Tong'

"""
url handlers
"""
import time, json, logging, hashlib, base64, asyncio
from coroweb import get, post
from models import User, Comment, Blog, next_id
import orm


@get('/')
async def index(request):
    users = await User.findAll()

    return {
        '__template__': 'test.html',
        'users': users
    }

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b'Hello World']


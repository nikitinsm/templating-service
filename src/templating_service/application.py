# -*- coding: utf-8 -*-
import json
import mimetypes
import os
import time
import datetime

from werkzeug.exceptions import BadRequest, MethodNotAllowed, InternalServerError
from werkzeug.wrappers import Request, Response
from jinja2 import Environment, FileSystemLoader


# Settings

DEBUG = \
    (os.environ.get('DEBUG', '0').lower() in {'1', 'on', 'true'}) \
    or False

TEMPLATING_ROOT = \
    os.environ.get('TEMPLATING_ROOT') \
    or '/templates'

ALLOWED_METHODS = \
    {'post', 'get'}

MEASURE_DURATION = \
    DEBUG \
    or (os.environ.get('MEASURE_DURATION', '0').lower() in {'1', 'on', 'true'}) \
    or False


# Configure jinja environment

jinja_env = Environment\
    ( loader=FileSystemLoader(TEMPLATING_ROOT)
    )

jinja_env.globals['now'] = datetime.datetime.now


# Utils

def template(name, context):
    template_instance = jinja_env.get_template(name)
    return template_instance.render\
        ( **context
        )


# Server

@Request.application
def application(request):
    start = None
    if MEASURE_DURATION:
        start = time.time()

    # Get request

    method = request.environ['REQUEST_METHOD']
    if method.lower() not in ALLOWED_METHODS:
        return MethodNotAllowed()

    try:
        name = request.environ['PATH_INFO']
        assert name, 'Name required'
    except Exception as e:
        return InternalServerError('%s "%s"' % (repr(e), e.message))

    # Prepare template context

    try:
        context = request.data and json.loads(request.data) or {}
        assert type(context) is dict, 'Expected context as a mapping'
    except Exception as e:
        return BadRequest('Bad json: "%s"' % e.message)

    # Render

    try:
        data = template(name, context)
    except Exception as e:
        message = ''
        if DEBUG:
            message = '%s "%s"' % (repr(e), e.message)
        return InternalServerError(message)

    # Output

    mimetype = (mimetypes.guess_type(name) or ('text/plain', None))[0]
    headers =\
        { 'Access-Control-Allow-Origin': '*'
        , 'Access-Control-Allow-Headers': 'Content-Type'
        }

    # Prepare execution time

    if start:
        headers['Duration'] = time.time() - start

    return Response\
        ( data
        , mimetype=mimetype
        , headers=headers
        )

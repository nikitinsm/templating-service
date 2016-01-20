#!/usr/bin/env bash

gunicorn -b 0.0.0.0:80 -k eventlet templating_service.application
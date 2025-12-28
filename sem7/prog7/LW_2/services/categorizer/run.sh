#!/bin/sh
PORT=${PORT:-8080}
exec gunicorn --bind "0.0.0.0:${PORT}" --workers 2 --timeout 120 --access-logfile - services.categorizer.app:app


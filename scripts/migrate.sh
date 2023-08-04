#!/bin/sh

makemagrations.sh
python manage.py migrate --noinput
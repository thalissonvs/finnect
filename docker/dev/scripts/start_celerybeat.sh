#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

python manage.py migrate django_celery_beat
rm -rf './celerybeat.pid'

celery -A finnect.celery_app beat --loglevel=INFO
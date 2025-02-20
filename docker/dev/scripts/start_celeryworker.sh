#!/bin/bash

set -o errexit
set -o nounset

celery -A finnect.celery_app worker --loglevel=INFO
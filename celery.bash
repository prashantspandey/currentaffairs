#!/bin/bash
DJANGODIR=/home/ubuntu/currentaffairs
cd $DJANGODIR
source /home/ubuntu/currentaffairs/env/bin/activate
celery -A currentaffairs worker -l info

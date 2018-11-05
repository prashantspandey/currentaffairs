#!/bin/bash
DJANGODIR=/home/prashantbodhi/currentaffairs/currentaffairs
cd $DJANGODIR
source /home/prashantbodhi/currentaffairs/currentaffairs/env/bin/activate
celery -A currentaffairs worker -l info

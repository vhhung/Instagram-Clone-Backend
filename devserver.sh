#!/bin/sh
source .venv/bin/activate
export NAME=Hung
# export DATABASE_URL=mysql+pymysql://root:@localhost:3306/tralalerotralala
export DATABASE_URL=mysql+pymysql://root:hungdeptrai@35.221.136.148:3306/tralalerotralala
python -m flask --app main run --debug
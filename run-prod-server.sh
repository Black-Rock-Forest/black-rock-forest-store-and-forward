#!/bin/ash

python mqtt_sub.py &
python init_database.py
alembic upgrade head
flask run -p 2323 --host 0.0.0.0
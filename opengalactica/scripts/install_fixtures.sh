#!/usr/bin/env bash

pwd
./manage.py clean_database
./manage.py loaddata pds
./manage.py loaddata digitrox_ships
./manage.py loaddata extra_ships
./manage.py loaddata global_ships
./manage.py loaddata human_ships
./manage.py loaddata khaduuii_ships
./manage.py loaddata piraati_ships
./manage.py loaddata shin_ships
./manage.py loaddata zyk_ships

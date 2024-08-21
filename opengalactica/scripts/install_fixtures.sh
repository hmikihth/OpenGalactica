#!/usr/bin/env bash

pwd
./manage.py clean_database
echo "Load species"
./manage.py loaddata species

echo "Load planets"
./manage.py loaddata planets

echo "Load pds"
./manage.py loaddata pds

echo "Load digitrox_ships"
./manage.py loaddata digitrox_ships

echo "Load extra_ships"
./manage.py loaddata extra_ships

echo "Load global_ships"
./manage.py loaddata global_ships

echo "Load human_ships"
./manage.py loaddata human_ships

echo "Load khaduuii_ships"
./manage.py loaddata khaduuii_ships

echo "Load piraati_ships"
./manage.py loaddata piraati_ships

echo "Load shin_ships"
./manage.py loaddata shin_ships

echo "Load zyk_ships"
./manage.py loaddata zyk_ships

echo "Load fleets"
./manage.py loaddata fleets

#!/usr/bin/env bash

source $HOME/.local/bin/env

make install  

psql -a -d "$DATABASE_URL" -f database.sql
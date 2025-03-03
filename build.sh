#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh

source $HOME/.local/bin/env
export PATH="/opt/render/.local/bin:$PATH"

make install  

psql -a -d "$DATABASE_URL" -f database.sql
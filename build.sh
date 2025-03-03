#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh
which uv

echo 'bruh'

source $HOME/.local/bin/env
export PATH="/opt/render/.local/bin:$PATH"
source .venv/bin/activate
which uv
make install  

psql -a -d "$DATABASE_URL" -f database.sql
curl -LsSf https://astral.sh/uv/install.sh | sh

. $HOME/.local/bin/env

source

make install && psql -a -d $DATABASE_URL -f database.sql
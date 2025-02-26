#!/usr/bin/env bash

# Устанавливаем uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Добавляем uv в PATH
export PATH="$HOME/.local/bin:$PATH"

# Создаем виртуальное окружение
uv venv .venv

# Активируем виртуальное окружение
source .venv/bin/activate

# Устанавливаем зависимости из pyproject.toml
uv sync
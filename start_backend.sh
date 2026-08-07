#!/bin/zsh

set -e

read -s "DB_PASSWORD?MariaDB-Passwort: "
echo

export DB_PASSWORD

exec .venv/bin/python -m uvicorn backend.app.main:app --reload

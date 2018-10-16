#!/usr/bin/env bash

echo "Testing Code"
pipenv run python -m pytest tests/ -vv

echo "Validating Questions"
pipenv run python -m uploader.question_validator
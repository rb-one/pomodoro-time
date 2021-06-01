#!/bin/bash
source .venv/bin/activate
#pip install -r requierements.txt

# Initial development configuration
export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_ENV=development

# Email Configuration
# export APP_MAIL_USERNAME="your email here"
# export APP_MAIL_PASSWORD="your email password"
# export APP_DEFAULT_SENDER="your email here again"

flask run

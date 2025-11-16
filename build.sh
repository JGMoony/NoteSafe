#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Fix SocialApp BEFORE loading it
sed -i "s/ENV_GOOGLE_CLIENT_ID/$GOOGLE_CLIENT_ID/g" users/fixtures/socialapp.json
sed -i "s/ENV_GOOGLE_CLIENT_SECRET/$GOOGLE_CLIENT_SECRET/g" users/fixtures/socialapp.json

python manage.py loaddata users/fixtures/socialapp.json

#!/bin/bash

exec node app.js -k "${ACCESS_TOKEN}" -c "${VERSE_CRON}"

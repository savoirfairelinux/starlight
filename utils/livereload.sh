#!/bin/sh

if [ "$USE_HOT_RELOAD" != "true" ]; then
  exit 0
fi

cd /code
npm run webpack:dev


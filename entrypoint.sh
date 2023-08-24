#!/usr/bin/env bash

# load the virtualenv
source /app/venv/bin/activate

# make sure we respect ctrl+c for graceful shutdowns
function shutdown {
  kill -s SIGTERM $!
  exit 0
}

trap shutdown SIGINT SIGTERM

# run the streamlit app server
/app/venv/bin/python -m streamlit run streamlit-prettymapp/app.py

FROM python:slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
  python3-pip python3-venv make && \
  rm -rf /var/lib/apt/lists/*

# Install streamlit deps
RUN python3 -m venv /app/venv && \
  . /app/venv/bin/activate && \
  pip install --upgrade pip streamlit streamlit-image-select --no-cache-dir


# Add a non-root user and drop root privileges
RUN useradd -m app && \
  chown -R app:app /app
COPY --chown=app:app . /app
USER app

# Install dependencies
RUN . /app/venv/bin/activate && \
  make setup

# Run the app
EXPOSE 8501
CMD ["/app/venv/bin/python", "-m", "streamlit", "run", "streamlit-prettymapp/app.py"]
FROM python:3-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  libffi-dev python3-dev python3-pip python3-venv make cmake

# Install streamlit deps
RUN --mount=type=cache,mode=0755,target=/app/.cache/pip \
  python3 -m venv /app/venv && \
  . /app/venv/bin/activate && \
  pip install --upgrade pip streamlit streamlit-image-select && \
  rm -rf /app/venv/lib/python3.*/site-packages/**/tests

COPY . /app

# Install dependencies
RUN --mount=type=cache,mode=0755,target=/app/.cache/pip . /app/venv/bin/activate && \
  make setup

FROM python:3-slim as runtime

# Add a non-root user and drop root privileges
RUN useradd -m app -d /app
COPY --chown=app:app --from=builder /app /app

USER app
WORKDIR /app

# Run the app
EXPOSE 8501
CMD ["./entrypoint.sh"]
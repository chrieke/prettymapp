FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install the prettymapp package from the local source (not PyPI) so the app
# and the library can never drift apart, plus the webapp-only dependencies.
COPY pyproject.toml README.md ./
COPY prettymapp ./prettymapp/
COPY streamlit-prettymapp ./streamlit-prettymapp/

RUN pip3 install --no-cache-dir . streamlit==1.52.2 streamlit-image-select==0.6.0 pyogrio

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit-prettymapp/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

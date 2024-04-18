FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY streamlit-prettymapp /app/streamlit-prettymapp/

WORKDIR /app

RUN pip3 install -r streamlit-prettymapp/requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit-prettymapp/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

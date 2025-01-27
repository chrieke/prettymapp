FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY streamlit-prettymapp /app/streamlit-prettymapp/

WORKDIR /app

RUN pip3 install -r streamlit-prettymapp/requirements.txt
RUN pip3 install fastapi uvicorn

EXPOSE 8501
EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["uvicorn", "prettymapp.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]

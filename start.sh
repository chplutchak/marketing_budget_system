#!/bin/bash

# Run database migrations
alembic upgrade head

# Start both FastAPI and Streamlit
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} &
streamlit run streamlit_app/main.py --server.port 8501 --server.address 0.0.0.0
FROM python:3.10 as python-base
RUN mkdir user_management_service
WORKDIR  /user_management_service
COPY poetry.lock pyproject.toml ./
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

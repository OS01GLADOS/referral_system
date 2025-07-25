FROM python:3.11.9 as compile-image

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

COPY . /app/



FROM python:3.11.9 as build-image

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY --from=compile-image /opt/venv /opt/venv
# Make sure scripts in .local are usable:
WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"
CMD ["sh", "entrypoint.sh"]
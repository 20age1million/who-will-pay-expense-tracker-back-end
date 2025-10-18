FROM python:3.12-slim as base
WORKDIR /app

COPY . /app

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

EXPOSE 5100

RUN chmod +x scripts/entrypoint.sh

ENTRYPOINT [ "/app/scripts/entrypoint.sh" ]

CMD [ "python", "app.py" ]

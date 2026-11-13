FROM python:3.13-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project
COPY README.md LICENSE ./
COPY src ./src
RUN uv sync --locked --no-dev --no-editable

FROM python:3.13-slim
RUN useradd --create-home app && mkdir -p /app/data && chown app:app /app/data
COPY --from=build /app/.venv /app/.venv
USER app
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["expenses"]
CMD ["--help"]

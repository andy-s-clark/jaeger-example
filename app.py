#!/usr/bin/env python3
from os import environ

from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from uvicorn import run

config = {
    "agent_host_name": environ.get("AGENT_HOST_NAME", "localhost"),
    "agent_port": int(environ.get("AGENT_PORT", "6831")),
}

trace.set_tracer_provider(
    TracerProvider(resource=Resource.create())
)

jaeger_exporter = JaegerExporter(
    agent_host_name=config["agent_host_name"],
    agent_port=config["agent_port"]
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("startup"):
    print("Startup test")

# TODO Export directly to Jaeger Collector
# TODO Specify agent/collector config for FastAPI instrumentation

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/config")
async def get_config():
    return config


@app.get("/docs")
async def get_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/health")
async def get_health():
    return {"status": "OK"}


@app.get("/openapi.json", tags=["documentation"])
async def get_open_api_endpoint():
    return JSONResponse(get_openapi(title="Jaeger-Example", version="1", routes=app.routes))


@app.get("/throw-error")
def get_throw_error():
    raise HTTPException(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Intentionally throwing an internal error response."
    )


FastAPIInstrumentor.instrument_app(app)

if __name__ == "__main__":
    run("app:app", port=8000, reload=False, debug=True, workers=1)

OTEL_RESOURCE_ATTRIBUTES=service.name=com.github.rhildred.INFO8985_microservice_analysis,service.version=de732a0 OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 OTEL_EXPORTER_OTLP_PROTOCOL=grpc OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true OTEL_EXPORTER_OTLP_INSECURE=true opentelemetry-instrument --logs_exporter otlp uvicorn app:app --host localhost --port 5002

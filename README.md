# telemetry-core

Commercial Fleet Tracking - Vehicle Telemetry Ingestion Service.

Automated CI/CD pipeline to test, containerize, and orchestrate vehicle telemetry ingestion services reliably across distributed compute clusters.

## Architecture
- **Service**: `telemetry-core`
- **Component**: Vehicle Telemetry Ingestion Engine
- **Default Port**: 9092
- **Config**: `telemetry.conf`

## Configuration
The service reads port and cluster settings from `telemetry.conf`:
```properties
TELEMETRY_PORT=9092
```

## Getting Started
```cmd
python app.py
```

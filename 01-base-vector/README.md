# Scenario 01 – Base Vector: Dynamic NSP Telemetry Observability Pipeline

**NSP Kafka → Vector (VRL) → Prometheus → Grafana**


## Overview

This proof-of-concept demonstrates how to transform **Kafka-based telemetry from Nokia NSP** into **Prometheus-compatible metrics** using [Vector.dev](https://vector.dev/) with [Vector Remap Language (VRL)](https://vector.dev/docs/reference/vrl/).

The telemetry source is **Nokia Network Services Platform (NSP)**, which streams structured JSON metrics from network elements via Kafka.
The goal of this scenario is to validate a **generic transformation pipeline** that avoids building custom logic for each metric type.

Instead of writing individual mappers (as is required in tools like Telegraf), **Vector applies a single dynamic VRL transform** to normalize any compatible JSON metric in real time and expose it as a Prometheus metric.

> 💡 **Key idea:** Use a single VRL transform to generically normalize all NSP telemetry into Prometheus format—**no per-metric configuration required**.

This scenario also includes **prebuilt Grafana dashboards** for immediate visualization of metrics like periodic CPU and memory usage.

### Demo
https://github.com/user-attachments/assets/382274fb-7d63-46d7-9805-2dc8b2ef4f3b

## Architecture

```
NSP Kafka → Vector (input → VRL transform → Prometheus sink) → Prometheus → Grafana
```

* **NSP** emits telemetry in structured JSON via Kafka.
* **Vector** consumes topics and applies VRL-based normalization.
* **Prometheus** scrapes Vector’s Prometheus sink endpoint.
* **Grafana** visualizes the results using predefined dashboards.


## Why It Matters

Traditional telemetry stacks often require:

* Custom logic or plugins per metric
* Manual updates when new metrics are introduced

This PoC addresses those challenges by providing:

✅ **One VRL transform for all metrics**
✅ **Schema-resilient transformation logic**
✅ **Dynamic pipeline extensibility with minimal code**

It’s lightweight, scalable, and well-suited for evolving NSP telemetry models.


## Quick Start

### 1. Retrieve NSP Kafka Certificates

Extract the necessary TLS certificates from your NSP Kubernetes cluster (tested on NSP 24.11):

```bash
kubectl cp $(kubectl get pods --all-namespaces | grep nspos-postgresql-primary-0 | awk '{ print $2 }'):/opt/nsp/os/ssl/ca_cert.pem ./certs/ca_cert.pem -n nsp-psa-restricted
kubectl cp $(kubectl get pods --all-namespaces | grep nspos-postgresql-primary-0 | awk '{ print $2 }'):/opt/nsp/os/ssl/nsp.key ./certs/nsp.key -n nsp-psa-restricted
kubectl cp $(kubectl get pods --all-namespaces | grep nspos-postgresql-primary-0 | awk '{ print $2 }'):/opt/nsp/os/ssl/nsp_external_combined.pem ./certs/nsp_external_combined.pem -n nsp-psa-restricted
```

### 2. Configure Environment Variables

Edit `configs/environment.env`:

```env
NSP_IP=10.1.2.10
NSP_KAFKA_PORT=9192
KAFKA_TOPICS=" \"topic-01\", \"topic-02\" "
```

### 3. Deploy the Topology

Launch the telemetry stack using Containerlab:

```bash
containerlab deploy -t nokia-nsp-telemetry.clab.yaml
```

### 4. Verify Kafka Connectivity (Optional)

```bash
kaf topics
kaf consume $KAFKA_TOPICS --timeout 5s
kaf consume $KAFKA_TOPICS --offset newest -n 2 -v
```

### 5. Explore Grafana

Open Grafana via the IP of the **Containerlab host**. The following dashboards are included:

* **CPU Usage (Periodic)**
* **Memory Usage (Periodic)**


## Containerlab Details

This scenario uses [Containerlab](https://containerlab.dev/) for reproducible testbed deployment.

### Host Network Mode

All containers run using `network_mode: host` to simplify inter-container communication and TLS-based Kafka access.

```bash
containerlab deploy -t nokia-nsp-telemetry.clab.yaml
```


## Dashboards

Grafana includes two example dashboards:

* **CPU Usage Periodic**
* **Memory Usage Periodic**

These panels are mapped to metrics normalized by Vector using VRL. You can easily extend or clone these dashboards to visualize other telemetry fields.

## Troubleshooting

| Symptom                    | Likely Cause                       | Suggested Fix                                                    |
| -------------------------- | ---------------------------------- | ---------------------------------------------------------------- |
| Vector Kafka errors        | Wrong IP, port, or missing certs   | Double-check `environment.env` and `certs/` paths                |
| Prometheus missing metrics | VRL logic failed or topic is empty | Run `vector validate vector.toml`; check topic content via `kaf` |
| Grafana shows no data      | Prometheus scraping issue          | Check Prometheus targets and test queries manually               |
| `kaf` can’t consume topics | TLS error or topic mismatch        | Use `kaf topics` to confirm topic names and TLS config           |


## Summary

This scenario proves that with **Vector and VRL**, it's possible to dynamically convert Nokia NSP’s structured Kafka telemetry into Prometheus metrics without per-metric mapping or manual scrapers. It serves as a **foundational pattern** for building more advanced pipelines (e.g., enrichment, gNMI support, or hybrid collectors).


## Disclaimer

The code and configurations in this scenario are provided for **proof-of-concept purposes only** and come with no warranties, express or implied. Use of this material is at your own risk. The authors and their employers assume no responsibility for any loss or disruption. Always validate thoroughly before considering any use in production environments.
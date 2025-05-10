# Nokia NSP Telemetry Observability Scenarios

This repository contains a collection of **modular, proof-of-concept telemetry pipeline scenarios** built around **Nokia NSP (Network Services Platform)** telemetry. Each scenario demonstrates how structured telemetry—exported via Kafka from NSP—can be integrated with modern open-source observability tools such as **Vector**, **gNMIc**, **Prometheus**, and **Grafana**.

These scenarios serve as **practical, reproducible demonstrations** of various telemetry processing techniques, including dynamic transformation with VRL, enrichment, and flexible exporter configurations. While some patterns may align with production practices, these examples are intended as **proof-of-concept workflows** to support evaluation, experimentation, and learning.

> ✅ All scenarios are packaged using [Containerlab](https://containerlab.dev/) to ensure isolated, repeatable, and easily deployable lab environments.


## Scenarios

| Scenario Folder               | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| [`01-base-vector/`](./scenarios/01-base-vector)           | Basic telemetry pipeline: NSP Kafka → Vector (VRL) → Prometheus → Grafana |
| _[more coming soon]_         | Planned scenarios: Vector with enrichment, Uses gNMIc instead Vector, etc.    |


## Prerequisites

- Access to a **Nokia NSP deployment** (e.g., version 24.11 or later)
- Kubernetes access to extract NSP Kafka TLS certificates
- Docker and [Containerlab](https://containerlab.dev/) installed
- Optional: Access to real telemetry-generating network elements


## Project Structure

```bash
nokia-nsp-telemetry/
├── scenarios/              # Individual, self-contained PoC scenarios
│   ├── base-vector/
│   ├── vector-with-enrichment/
│   └── ...
├── shared/                 # Common certs, VRL templates, docs, visuals
├── Makefile                # Optional: helper targets to deploy/destroy
├── LICENSE
└── README.md               # This file
````

## Getting Started

1. Clone the repo:

   ```bash
   git clone https://github.com/asadarafat/nokia-nsp-telemetry.git
   cd nokia-nsp-telemetry
   ```

2. Choose a scenario:

   ```bash
   cd scenarios/01-base-vector
   ```

3. Follow the `README.md` in that folder to deploy the pipeline using Containerlab.


## Contributing

Have an idea for another scenario—like NetFlow export, OTel integration, or log correlation?
Feel free to fork the repo and submit a pull request.

Please keep scenarios:

* Self-contained
* Lightweight and reproducible
* Documented and versioned clearly


## License

This project is licensed under the [MIT License].


## Disclaimer

The code and configurations in this repository are provided for **proof-of-concept purposes only** and come with no warranties, express or implied. Use of this material is at your own risk; the authors and their employers assume no liability for any loss or damage resulting from its use. You are responsible for ensuring compliance with all applicable laws, regulations, and internal policies. No support or maintenance is guaranteed—always test thoroughly before using in any production environment.
# Kubernetes Redis Counter API

[![Build and Push Multi-Arch Docker Image](https://github.com/rafilkmp3/kubernetes-redis-counter-api/actions/workflows/docker-image.yml/badge.svg)](https://github.com/rafilkmp3/kubernetes-redis-counter-api/actions/workflows/docker-image.yml)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple API that increments a counter persisted in Redis, containerized and designed for deployment to Kubernetes using Helm.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Usage](#detailed-usage)
  - [Local Development](#local-development)
  - [Using Your Own Image](#using-your-own-image)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Helm Chart Configuration](#helm-chart-configuration)
- [CI/CD](#cicd)
- [Security Considerations](#security-considerations)
- [Scalability](#scalability)
- [Contributing](#contributing)
- [License](#license)

## Features

- RESTful API with `/read` and `/write` endpoints
- Counter value persisted in Redis
- Containerized application
- Kubernetes deployment ready
- Helm charts for easy deployment
- Horizontal Pod Autoscaling
- Liveness and Readiness probes
- Multi-architecture Docker image support (amd64, arm64, arm/v7)

## Prerequisites

- Docker
- Minikube (for local development)
- Helm 3
- kubectl

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/rafilkmp3/kubernetes-redis-counter-api.git
   cd kubernetes-redis-counter-api
   ```

2. Start Minikube:
   ```bash
   minikube start
   ```

3. Deploy the application:
   ```bash
   helm repo add stakater https://stakater.github.io/stakater-charts
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo update
   helm upgrade --install counter-api ./helm/ -f ./helm/values.yaml
   ```

4. Access the API:
   ```bash
   kubectl port-forward svc/counter-api 8080:80 &
   curl http://localhost:8080/read
   ```

5. When you're done, stop the port forwarding:
   ```bash
   pkill -f "kubectl port-forward svc/counter-api"
   ```

## Detailed Usage

### Local Development

1. Configure your terminal to use Minikube's Docker daemon:
   ```bash
   eval $(minikube docker-env)
   ```

2. Build the Docker image:
   ```bash
   docker build -t ghcr.io/rafilkmp3/kubernetes-redis-counter-api:latest . --no-cache
   ```

3. Update `helm/values.yaml`:
   ```yaml
   application:
     deployment:
       image:
         repository: ghcr.io/rafilkmp3/kubernetes-redis-counter-api
         tag: latest
         pullPolicy: Never
   ```

4. Deploy and test as described in the Quick Start section.

5. Remember to stop the port forwarding when you're done:
   ```bash
   pkill -f "kubectl port-forward svc/counter-api"
   ```

### Using Your Own Image

1. Build your custom image:
   ```bash
   docker build -t your-registry/your-image:your-tag .
   ```

2. Update `helm/values.yaml` or use `--set` with Helm:
   ```bash
   helm upgrade --install counter-api ./helm/ -f ./helm/values.yaml \
     --set application.deployment.image.repository=your-registry/your-image \
     --set application.deployment.image.tag=your-tag
   ```

## API Endpoints

- `GET /read`: Returns the current counter value
- `POST /write`: Increments the counter value
- `GET /healthz`: Health check endpoint
- `GET /ready`: Readiness check endpoint

## Deployment

For production deployment, ensure you have a Kubernetes cluster running and `kubectl` configured. Then follow the steps in the Quick Start section, adjusting the Helm values as needed for your environment.

## Helm Chart Configuration

Key configuration options in `values.yaml`:

- Redis: Standalone architecture, authentication disabled
- Application: 2 replicas, HPA enabled (2-10 replicas), resource limits defined

For full configuration options, refer to the `values.yaml` file in the `helm` directory.

## CI/CD

This project uses GitHub Actions for CI/CD. The workflow builds and pushes a multi-architecture Docker image to GitHub Container Registry on pushes to the `main` branch.

For details, see [.github/workflows/docker-image.yml](.github/workflows/docker-image.yml).

## Security Considerations

- Implement authentication for production use
- Enable Redis authentication for production
- Configure HTTPS/TLS for production deployments

## Scalability

- HPA configured for 2-10 replicas
- Consider implementing a Redis cluster for high availability
- Optimize resource requests/limits based on usage patterns

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
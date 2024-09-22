# Kubernetes Redis Counter API

This project implements a simple API that increments a counter persisted in Redis. The API is containerized and designed to be deployed to Kubernetes using Helm.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
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
- Multi-architecture Docker image support

## Prerequisites

- Docker
- Minikube
- Helm 3
- kubectl

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/rafilkmp3/kubernetes-redis-counter-api.git
   cd kubernetes-redis-counter-api
   ```

2. Build and push the Docker image (if not using the pre-built image):
   ```
   docker build -t ghcr.io/rafilkmp3/kubernetes-redis-counter-api:latest .
   docker push ghcr.io/rafilkmp3/kubernetes-redis-counter-api:latest
   ```

## Usage

### Local Development

1. Start Minikube:
   ```
   minikube start
   ```

2. Deploy the application using Helm:
   ```
   helm upgrade --install counter-api ./helm/ -f ./helm/values.yaml
   ```

3. Set up port forwarding to access the service:
   ```
   kubectl port-forward svc/counter-api 8080:80 &
   ```
   This command will run in the background and forward local port 8080 to the service's port 80.

4. Access the API endpoints:
   - To read the counter value:
     ```
     curl http://localhost:8080/read
     ```
   - To increment the counter:
     ```
     curl -X POST http://localhost:8080/write
     ```

5. To stop port forwarding when you're done:
   ```
   pkill -f "kubectl port-forward svc/counter-api"
   ```

Note: The port-forwarding process will continue running in the background. Make sure to stop it when you're finished working with the service.

## API Endpoints

- GET `/read`: Returns the current counter value
- POST `/write`: Increments the counter value
- GET `/healthz`: Health check endpoint
- GET `/ready`: Readiness check endpoint

## Deployment

1. Ensure you have a Kubernetes cluster running and `kubectl` configured.

2. Add the required Helm repositories:
   ```
   helm repo add stakater https://stakater.github.io/stakater-charts
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo update
   ```

3. Deploy or upgrade the Helm chart:
   ```
   helm upgrade --install counter-api ./helm/ -f ./helm/values.yaml
   ```

4. Verify the deployment:
   ```
   kubectl get pods
   kubectl get services
   ```

## Helm Chart Configuration

The Helm chart (version 0.1.0) is configured with the following dependencies:
- Application chart from Stakater (version ~4.2.8)
- Redis chart from Bitnami (version ~17.9.3)

Key configuration options in `values.yaml`:

- Redis:
  - Standalone architecture
  - Authentication disabled
  - Persistence disabled

- Application:
  - 2 replicas by default
  - Environment variables for Redis connection
  - Liveness and Readiness probes configured
  - Resource limits and requests defined
  - Horizontal Pod Autoscaling enabled (2-10 replicas)
  - PodDisruptionBudget configured
  - NodePort service type

To customize the deployment, modify the `values.yaml` file before installing the Helm chart.

## CI/CD

This project uses GitHub Actions for continuous integration and deployment. The workflow automatically builds and pushes a multi-architecture Docker image to the GitHub Container Registry (ghcr.io) when changes are pushed to the main branch.

### Workflow Details

- **Trigger**: Push to the `main` branch
- **Runner**: Ubuntu Latest
- **Steps**:
  1. Checkout code
  2. Set up QEMU for multi-architecture support
  3. Set up Docker Buildx
  4. Log in to GitHub Container Registry
  5. Build and push Docker image
  6. Verify Docker image

### Multi-Architecture Support

The Docker image is built for the following architectures:
- linux/amd64
- linux/arm64
- linux/arm/v7

### Image Tags and Labels

- The image is tagged as `latest`
- Labels are added for OpenContainers metadata

To view the full workflow configuration, check the `.github/workflows/docker-build-push.yml` file in the repository.

## Security Considerations

- The API doesn't implement authentication. Consider adding an auth layer for production use.
- Redis authentication is disabled by default. Enable it for production deployments.
- HTTPS is not configured. Add TLS for production deployments.

## Scalability

The application is configured with Horizontal Pod Autoscaling:
- Minimum replicas: 2
- Maximum replicas: 10

To further improve scalability:
1. Adjust HPA settings in `values.yaml` if needed.
2. Consider implementing a Redis cluster for high availability.
3. Optimize resource requests and limits based on actual usage patterns.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
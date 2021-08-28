# otusidempotence

# Теория

# Prerequisites

* Kubernetes 1.21.2
* Helm 3.6.3
* Istio 1.10.3
* Skaffold

# Run

## Add Helm repos

```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add kiali https://kiali.org/helm-charts
helm repo add jaeger https://jaegertracing.github.io/helm-charts
helm repo add prometheus https://prometheus-community.github.io/helm-charts
```

## Create k8s namespaces

```
kubectl apply -f deployments/k8s/namespaces.yaml
```

## Run with Skaffold

```
skaffold run
```

# Tests

```
newman run orders.postman_collection.json
```

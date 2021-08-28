#!/bin/bash
set -e

DIST=dist

ISTIO_VERSION=1.10.3
ISTIO_DIR="${DIST}/istio-${ISTIO_VERSION}"
ISTIOCTL="${ISTIO_DIR}/bin/istioctl"

ADDONS="prometheus grafana jaeger kiali"
NAMESPACE="istio-system"

if [[ ! -f "${ISTIOCTL}" ]]; then
  cd ${DIST} && curl -L https://istio.io/downloadIstio | ISTIO_VERSION=${ISTIO_VERSION} sh -
fi

echo Creating the control plane namespace: ${NAMESPACE}

if ! kubectl get namespace ${NAMESPACE}; then
  kubectl create namespace ${NAMESPACE}
fi

echo "Installing Istio ${ISTIO_VERSION}"
${ISTIOCTL} install --set profile=demo --istioNamespace=${NAMESPACE} --skip-confirmation

echo "Installing Addons: [${ADDONS}]"
for addon in ${ADDONS}; do
  echo "Installing addon: [${addon}]"
  while ! (cat ${ISTIO_DIR}/samples/addons/${addon}.yaml | sed "s/istio-system/${NAMESPACE}/g" | kubectl apply -n ${NAMESPACE} -f -)
  do
    echo "Failed to install addon [${addon}] - will retry in 10 seconds..."
    sleep 10
  done
done

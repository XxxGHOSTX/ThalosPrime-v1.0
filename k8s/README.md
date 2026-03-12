# Kubernetes Deployment for Thalos Prime

This directory contains Kubernetes manifests for deploying Thalos Prime in production.

## Manifests

- `00-namespace.yaml` - Namespace isolation
- `01-configmap.yaml` - Configuration
- `02-pvc.yaml` - Persistent volumes (sessions + logs)
- `03-deployment.yaml` - Application deployment
- `04-service.yaml` - ClusterIP service
- `05-rbac.yaml` - ServiceAccount, Role, RoleBinding
- `06-hpa.yaml` - Horizontal Pod Autoscaler (3-10 replicas)
- `07-pdb.yaml` - Pod Disruption Budget (min 2 available)

## Quick Deployment

```bash
# Deploy all resources
kubectl apply -f k8s/

# Verify deployment
kubectl get all -n thalos-prime

# Check pod status
kubectl get pods -n thalos-prime -w
```

## Configuration

Edit `01-configmap.yaml` to customize:
- Storage paths
- Log levels
- Application settings

## Scaling

The HPA automatically scales between 3-10 replicas based on:
- CPU utilization (target: 70%)
- Memory utilization (target: 80%)

Manual scaling:
```bash
kubectl scale deployment thalos-prime -n thalos-prime --replicas=5
```

See `docs/deployment.md` for detailed information.

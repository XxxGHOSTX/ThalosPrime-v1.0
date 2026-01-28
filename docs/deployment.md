# Production Deployment Guide

## Overview

This guide covers deploying Thalos Prime v1.0 in production environments.

## Prerequisites

- Python 3.8 or higher
- Git
- Docker (optional, for containerized deployment)
- Kubernetes (optional, for orchestration)

## Deployment Options

### 1. Standard Installation

```bash
# Clone repository
git clone https://github.com/XxxGHOSTX/ThalosPrime-v1.0.git
cd ThalosPrime-v1.0

# Run setup and verification
./setup_verify.sh

# Or install manually
pip install .

# Verify installation
thalos --version
```

### 2. Docker Deployment

```bash
# Build image
docker build -t thalos-prime:1.0.0 .

# Run container
docker run -d \
  --name thalos-prime \
  -v thalos-sessions:/app/.thalos/sessions \
  -v thalos-logs:/app/logs \
  -p 8000:8000 \
  thalos-prime:1.0.0

# Verify
docker exec thalos-prime thalos --version
```

### 3. Docker Compose Deployment

```bash
# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f thalos-prime

# Stop services
docker-compose down
```

### 4. Kubernetes Deployment

```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment
kubectl get pods -n thalos-prime

# View logs
kubectl logs -f deployment/thalos-prime -n thalos-prime

# Access service
kubectl port-forward svc/thalos-prime 8000:8000 -n thalos-prime
```

## Configuration

### Environment Variables

```bash
# Session storage directory
export THALOS_SESSION_DIR=/path/to/sessions

# Log directory
export THALOS_LOG_DIR=/path/to/logs

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
export THALOS_LOG_LEVEL=INFO

# API host (when implemented)
export THALOS_API_HOST=0.0.0.0
export THALOS_API_PORT=8000
```

### Configuration File

Create `config/production.yaml`:

```yaml
thalos:
  version: "1.0.0"
  
  session:
    storage_dir: "/var/lib/thalos/sessions"
    backup_enabled: true
    backup_interval: 3600
    max_sessions: 1000
  
  logging:
    level: "INFO"
    directory: "/var/log/thalos"
    format: "json"
    max_size_mb: 100
    backup_count: 10
  
  api:
    enabled: true
    host: "0.0.0.0"
    port: 8000
    cors_enabled: true
    auth_required: true
  
  security:
    token_expiry: 3600
    max_login_attempts: 5
    rate_limit_requests: 100
    rate_limit_period: 60
```

## Production Checklist

### Pre-deployment

- [ ] All tests passing
- [ ] Security scan completed
- [ ] Configuration reviewed
- [ ] Secrets properly managed
- [ ] Backup strategy defined
- [ ] Monitoring configured
- [ ] Documentation updated

### Deployment

- [ ] Infrastructure provisioned
- [ ] Services deployed
- [ ] Health checks passing
- [ ] Monitoring active
- [ ] Backups configured
- [ ] Alerts configured

### Post-deployment

- [ ] Smoke tests executed
- [ ] Performance validated
- [ ] Security audit completed
- [ ] Documentation updated
- [ ] Team notified

## Monitoring

### Health Checks

```bash
# CLI health check
thalos session status --all

# API health check (when implemented)
curl http://localhost:8000/health

# Docker health check
docker inspect --format='{{.State.Health.Status}}' thalos-prime
```

### Metrics

Monitor these key metrics:

- **Session metrics**:
  - Active sessions count
  - Session creation rate
  - Session termination rate
  - Session state distribution

- **Performance metrics**:
  - Response time
  - Throughput
  - Error rate
  - CPU usage
  - Memory usage

- **System metrics**:
  - Disk usage (session storage)
  - Network I/O
  - Process count

### Logging

Logs are stored in:
- Default: `./logs/`
- Docker: `/app/logs/`
- Custom: `$THALOS_LOG_DIR`

Log levels:
- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages
- `WARNING`: Warning messages (non-critical)
- `ERROR`: Error messages (recoverable)
- `CRITICAL`: Critical errors (system failure)

## Backup and Recovery

### Session Backup

```bash
# Backup sessions
tar -czf sessions-backup-$(date +%Y%m%d).tar.gz .thalos/sessions/

# Restore sessions
tar -xzf sessions-backup-20260128.tar.gz -C .thalos/
```

### Database Backup (future)

```bash
# PostgreSQL backup
docker exec thalos-postgres pg_dump -U thalos thalos_prime > backup.sql

# Redis backup
docker exec thalos-redis redis-cli SAVE
```

## Security

### Best Practices

1. **Use environment-specific configurations**
   ```bash
   export THALOS_ENV=production
   ```

2. **Secure secrets management**
   - Use environment variables for sensitive data
   - Use secrets management tools (HashiCorp Vault, AWS Secrets Manager)
   - Never commit secrets to version control

3. **Enable authentication**
   - Configure API authentication
   - Use strong tokens
   - Rotate credentials regularly

4. **Network security**
   - Use HTTPS in production
   - Configure firewall rules
   - Limit external access

5. **Regular updates**
   - Keep dependencies updated
   - Apply security patches
   - Monitor vulnerability reports

### Security Checklist

- [ ] Secrets stored securely
- [ ] Authentication enabled
- [ ] HTTPS configured
- [ ] Firewall rules applied
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Input validation enforced
- [ ] Audit logging enabled

## Scaling

### Horizontal Scaling

```yaml
# Kubernetes ReplicaSet
apiVersion: apps/v1
kind: Deployment
metadata:
  name: thalos-prime
spec:
  replicas: 3  # Scale to 3 instances
  ...
```

### Vertical Scaling

```yaml
# Increase resource limits
resources:
  limits:
    cpu: 4
    memory: 8Gi
  requests:
    cpu: 2
    memory: 4Gi
```

### Load Balancing

```yaml
# Kubernetes Service with LoadBalancer
apiVersion: v1
kind: Service
metadata:
  name: thalos-prime
spec:
  type: LoadBalancer
  ports:
  - port: 8000
    targetPort: 8000
```

## Troubleshooting

### Common Issues

**Issue**: CLI not found after installation
```bash
# Solution: Ensure PATH includes Python scripts directory
export PATH="$PATH:$HOME/.local/bin"
```

**Issue**: Permission denied on session storage
```bash
# Solution: Fix permissions
chmod 755 .thalos/
chmod 644 .thalos/sessions/*
```

**Issue**: Tests failing
```bash
# Solution: Reinstall dependencies
pip install -e ".[dev]"
pytest tests/ -v
```

**Issue**: Docker container not starting
```bash
# Solution: Check logs
docker logs thalos-prime

# Rebuild image
docker-compose build --no-cache
docker-compose up -d
```

### Debug Mode

```bash
# Enable debug logging
export THALOS_LOG_LEVEL=DEBUG

# Run with verbose output
thalos --verbose session status --all
```

## Performance Tuning

### Optimization Tips

1. **Session storage**
   - Use SSD for session storage
   - Regular cleanup of terminated sessions
   - Configure session TTL

2. **Memory management**
   - Set appropriate memory limits
   - Monitor memory usage
   - Enable swap if needed

3. **Concurrency**
   - Configure worker processes
   - Adjust thread pool size
   - Use async operations

4. **Caching**
   - Enable Redis caching (future)
   - Configure cache TTL
   - Monitor cache hit rate

## Support

For issues and questions:
- GitHub Issues: https://github.com/XxxGHOSTX/ThalosPrime-v1.0/issues
- Documentation: See `docs/` directory
- Security Issues: See SECURITY.md

## Maintenance

### Regular Tasks

- **Daily**: Review logs and metrics
- **Weekly**: Session cleanup, backup verification
- **Monthly**: Security updates, performance review
- **Quarterly**: Capacity planning, architecture review

### Update Procedure

```bash
# 1. Backup current installation
./scripts/backup.sh

# 2. Pull latest changes
git pull origin main

# 3. Install updates
pip install -e . --upgrade

# 4. Run tests
pytest tests/

# 5. Restart services
sudo systemctl restart thalos-prime
# or
docker-compose restart
```

## Production Examples

### systemd Service

Create `/etc/systemd/system/thalos-prime.service`:

```ini
[Unit]
Description=Thalos Prime Agent Session Manager
After=network.target

[Service]
Type=simple
User=thalos
Group=thalos
WorkingDirectory=/opt/thalos-prime
Environment="THALOS_SESSION_DIR=/var/lib/thalos/sessions"
Environment="THALOS_LOG_DIR=/var/log/thalos"
ExecStart=/usr/local/bin/thalos-server
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable thalos-prime
sudo systemctl start thalos-prime
sudo systemctl status thalos-prime
```

### Nginx Reverse Proxy

```nginx
upstream thalos_backend {
    server localhost:8000;
    # Add more servers for load balancing
    # server localhost:8001;
    # server localhost:8002;
}

server {
    listen 80;
    server_name thalos.example.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name thalos.example.com;
    
    ssl_certificate /etc/ssl/certs/thalos.crt;
    ssl_certificate_key /etc/ssl/private/thalos.key;
    
    location / {
        proxy_pass http://thalos_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (future)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

**Production deployment complete!** 🚀

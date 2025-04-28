# Docker Setup and Usage SOP

## Overview
This document outlines the standard operating procedures for containerizing and running the Flask application using Docker.

## Prerequisites
- Docker installed on your system
- Git repository cloned
- Python 3.9 or higher (for local development)

## Project Structure
```
.
├── app/                    # Application code
├── docs/                   # Documentation
├── logs/                   # Application logs
├── instance/              # Instance-specific files
├── Dockerfile             # Docker configuration
├── .dockerignore         # Docker ignore rules
└── requirements.txt      # Python dependencies
```

## Docker Configuration Files

### Dockerfile
The `Dockerfile` contains the following key components:
- Base image: Python 3.9-slim
- Working directory: `/app`
- Environment variables for Flask
- System dependencies installation
- Python dependencies installation
- Application files copying
- Port exposure: 5000
- Gunicorn server configuration

### .dockerignore
Excludes unnecessary files from the Docker build context:
- Git-related files
- Python cache and virtual environment
- Logs and instance folders
- IDE-specific files
- OS-specific files

## Building and Running the Container

### Building the Image
```bash
# Build the Docker image
docker build -t app .
```

### Running the Container
```bash
# Run the container
docker run -p 5000:5000 app
```

### Additional Run Options
```bash
# Run in detached mode
docker run -d -p 5000:5000 app

# Run with environment variables
docker run -p 5000:5000 -e FLASK_ENV=production app

# Run with volume mounting for logs
docker run -p 5000:5000 -v $(pwd)/logs:/app/logs app
```

## Container Management

### Viewing Running Containers
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a
```

### Stopping Containers
```bash
# Stop a running container
docker stop <container_id>

# Stop all running containers
docker stop $(docker ps -q)
```

### Removing Containers
```bash
# Remove a stopped container
docker rm <container_id>

# Remove all stopped containers
docker container prune
```

### Viewing Logs
```bash
# View container logs
docker logs <container_id>

# Follow container logs
docker logs -f <container_id>
```

## Best Practices

1. **Security**
   - Never run containers as root
   - Use specific version tags for base images
   - Regularly update base images and dependencies

2. **Performance**
   - Use multi-stage builds for smaller images
   - Implement proper caching strategies
   - Monitor container resource usage

3. **Development**
   - Use Docker Compose for local development
   - Implement health checks
   - Use environment variables for configuration

4. **Maintenance**
   - Regularly clean up unused images and containers
   - Monitor container logs
   - Keep documentation updated

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check if port 5000 is in use
   lsof -i :5000
   # Kill the process using the port
   kill -9 <PID>
   ```

2. **Container Won't Start**
   ```bash
   # Check container logs
   docker logs <container_id>
   # Check container status
   docker inspect <container_id>
   ```

3. **Build Failures**
   ```bash
   # Clean build cache
   docker builder prune
   # Rebuild with no cache
   docker build --no-cache -t your-app-name .
   ```

## Support
For any issues or questions regarding Docker setup and usage, please contact the development team or refer to the project's issue tracker. 
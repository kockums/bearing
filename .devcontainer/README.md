# =============================================================================

# Dev Container README

# =============================================================================

# Rite Development Container

This directory contains the configuration for the Rite development container, providing a consistent Python 3.15 development environment.

## Features

-   **Python 3.15** with all necessary development tools
-   **Poetry** for dependency management
-   **Pre-configured VS Code** with Python extensions
-   **Git** with Git LFS support
-   **GitHub CLI** for repository management
-   **Zsh with Oh My Zsh** for enhanced shell experience
-   **All development tools** pre-installed (Black, isort, Flake8, Pylint, Mypy, Pytest)

## Quick Start

### Prerequisites

-   Docker Desktop (or Docker Engine + Docker Compose)
-   Visual Studio Code
-   Dev Containers extension for VS Code

### Usage

1. Open the project in VS Code
2. Press `F1` and select `Dev Containers: Reopen in Container`
3. Wait for the container to build (first time takes a few minutes)
4. Start developing!

## Container Structure

```
.devcontainer/
├── devcontainer.json      # Dev container configuration
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Multi-container orchestration
├── post-create.sh         # Post-creation setup script (moved to bin/)
├── .dockerignore          # Files to exclude from build
└── README.md              # This file
```

## Configuration Files

### devcontainer.json

Main configuration file that defines:

-   Container name and workspace folder
-   VS Code extensions to install
-   VS Code settings
-   Port forwarding
-   Environment variables
-   Post-create commands

### Dockerfile

Defines the container image with:

-   Python 3.15 base image
-   System dependencies
-   Poetry installation
-   Non-root user setup
-   Zsh and Oh My Zsh
-   Development tools

### docker-compose.yml

Orchestrates the container with:

-   Volume mounts for workspace and caches
-   Port mappings
-   Environment variables
-   Resource limits
-   Network configuration

### bin/post-create.sh

Post-creation setup script (formerly `.devcontainer/post-create.sh`, now in `bin/`):

Setup script that runs after container creation:

-   Installs project dependencies
-   Sets up pre-commit hooks
-   Configures git
-   Verifies tool installations
-   Creates necessary directories

## Volumes

Persistent volumes are created for:

-   Bash history
-   Zsh history
-   Poetry cache
-   VS Code extensions

This ensures your development environment persists across container rebuilds.

## Port Forwarding

The following ports are forwarded:

-   **8000**: Documentation server
-   **8080**: Development server

## Environment Variables

Pre-configured environment variables:

-   `PYTHONPATH=/workspace/src`
-   `PYTHONDONTWRITEBYTECODE=1`
-   `PYTHONUNBUFFERED=1`
-   `RITE_ENV=development`
-   `POETRY_VIRTUALENVS_IN_PROJECT=true`

## Installed Tools

The container comes with these tools pre-installed:

-   Python 3.15
-   Poetry 1.8.0
-   Git with Git LFS
-   GitHub CLI
-   Zsh with Oh My Zsh
-   Build essentials (gcc, g++, make)
-   Development libraries

After running `post-create.sh`, these are also available:

-   Black (code formatter)
-   isort (import sorter)
-   Flake8 (linter)
-   Pylint (static analyzer)
-   Mypy (type checker)
-   Pytest (test framework)
-   Coverage (code coverage)
-   Pre-commit (git hooks)
-   All other dependencies from pyproject.toml

## Customization

### Adding Extensions

Edit `devcontainer.json` and add extension IDs to the `extensions` array:

```json
"extensions": [
  "ms-python.python",
  "your-publisher.your-extension"
]
```

### Changing Python Version

Edit `Dockerfile` and change the base image:

```dockerfile
FROM python:3.16-slim-bookworm
```

### Adding System Packages

Edit `Dockerfile` and add packages to the `apt-get install` command:

```dockerfile
RUN apt-get update && apt-get install -y \
    your-package \
    && apt-get clean
```

### Modifying Resource Limits

Edit `docker-compose.yml` and adjust the limits:

```yaml
deploy:
    resources:
        limits:
            cpus: "8"
            memory: 16G
```

## Troubleshooting

### Container won't build

1. Check Docker is running
2. Ensure you have enough disk space
3. Try rebuilding without cache: `Dev Containers: Rebuild Without Cache`

### Extensions not installing

1. Check your internet connection
2. Try rebuilding the container
3. Manually install extensions after container starts

### Permission errors

The container runs as non-root user `vscode` (UID 1000). If you encounter permission errors:

```bash
sudo chown -R vscode:vscode /workspace
```

### Poetry issues

If Poetry fails to install dependencies:

```bash
poetry cache clear pypi --all
poetry install --no-interaction --with dev
```

### Port conflicts

If ports 8000 or 8080 are already in use, edit `docker-compose.yml`:

```yaml
ports:
    - "8001:8000" # Use 8001 on host instead
```

## Best Practices

1. **Commit regularly**: Your work is in mounted volumes
2. **Use Git inside the container**: Pre-configured with correct line endings
3. **Run tests frequently**: Use `make test` or `pytest`
4. **Format on save**: VS Code is configured to auto-format
5. **Check types**: Run `make type-check` before committing
6. **Use pre-commit**: Hooks are automatically installed

## Performance Tips

1. Use `:cached` mount option for better performance (already configured)
2. Exclude unnecessary files in `.dockerignore`
3. Use persistent volumes for caches (already configured)
4. Adjust resource limits based on your system

## Security

The container:

-   Runs as non-root user by default
-   Uses minimal base image (slim-bookworm)
-   Only installs necessary packages
-   Cleans up apt cache to reduce attack surface
-   Uses specific version pins where appropriate

## Additional Resources

-   [VS Code Dev Containers Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
-   [Docker Documentation](https://docs.docker.com/)
-   [Poetry Documentation](https://python-poetry.org/docs/)
-   [Rite Documentation](../../README.md)

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review the main project documentation
3. Open an issue on GitHub
4. Contact the maintainers

---

**Note**: The container configuration is optimized for development. For production deployments, use the appropriate production Dockerfile and configurations.

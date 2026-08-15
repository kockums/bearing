# =============================================================================
# Development Container for Rite
# Python 3.12 Development Environment
# =============================================================================

FROM python:3.12-slim-bookworm

# Metadata
LABEL maintainer="Scape Agency"
LABEL description="Rite Python 3.12 Development Container"
LABEL version="1.0"

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.0 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH="/opt/poetry/bin:${PATH}"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Build essentials
    build-essential \
    gcc \
    g++ \
    make \
    # Git
    git \
    git-lfs \
    # Shell and utilities
    zsh \
    curl \
    wget \
    ca-certificates \
    gnupg \
    lsb-release \
    # Editor
    nano \
    vim \
    # Process management
    procps \
    # Network tools
    net-tools \
    iputils-ping \
    # Development libraries
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && chmod +x /opt/poetry/bin/poetry

# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/zsh \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Oh My Zsh for the user
USER $USERNAME
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Configure Zsh
RUN echo 'export PYTHONPATH="/workspace/src:$PYTHONPATH"' >> ~/.zshrc \
    && echo 'export PATH="/opt/poetry/bin:$PATH"' >> ~/.zshrc \
    && echo 'alias ll="ls -lah"' >> ~/.zshrc \
    && echo 'alias pytest="poetry run pytest"' >> ~/.zshrc \
    && echo 'alias black="poetry run black"' >> ~/.zshrc \
    && echo 'alias isort="poetry run isort"' >> ~/.zshrc \
    && echo 'alias mypy="poetry run mypy"' >> ~/.zshrc \
    && echo 'alias flake8="poetry run flake8"' >> ~/.zshrc \
    && echo 'alias pylint="poetry run pylint"' >> ~/.zshrc

# Set working directory
WORKDIR /workspace

# Switch back to root for any remaining setup
USER root

# Install global Python tools (optional, for IDE support)
RUN pip install --no-cache-dir \
    pip-tools \
    pipx

# Switch to non-root user
USER $USERNAME

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python3 --version || exit 1

# Default command
CMD ["/bin/zsh"]

# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# --- Builder Stage ---
# This stage installs all build dependencies and compiles all Python versions.
FROM marketplace.gcr.io/google/ubuntu2404 AS builder

# TODO(https://github.com/googleapis/librarian/issues/901): Install the necssary dependencies and build tools.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # Essential for compiling C code
    build-essential \
    # For downloading secure files
    wget \
    ca-certificates \
    # For running bazelisk commands
    openjdk-17-jdk \
    # --- Critical libraries for a complete Python build ---
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libffi-dev \
    libsqlite3-dev \
    libreadline-dev \
    # ------------------------------------------------------
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up environment variables for tool versions to make updates easier.
ENV BAZELISK_VERSION=v1.26.0

# Install multiple Python versions from source. `make altinstall` is used to
# prevent replacing the system's default python binary.
RUN for PYTHON_VERSION in 3.9.23 3.10.18 3.11.13 3.12.11 3.13.5; do \
    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations --prefix=/usr/local && \
    make -j$(nproc) && \
    make altinstall && \
    cd / && \
    rm -rf Python-${PYTHON_VERSION}* \
    ; done

# Install pip for each python version
RUN wget --no-check-certificate -O /tmp/get-pip.py 'https://bootstrap.pypa.io/get-pip.py' && \
    for PYTHON_VERSION in 3.9 3.10 3.11 3.12 3.13; do \
        python${PYTHON_VERSION} /tmp/get-pip.py; \
    done && \
    rm /tmp/get-pip.py

# Install Bazelisk
RUN wget https://github.com/bazelbuild/bazelisk/releases/download/${BAZELISK_VERSION}/bazelisk-linux-amd64 -O /usr/local/bin/bazelisk && \
    chmod +x /usr/local/bin/bazelisk

# Set the working directory for build-related tasks.
WORKDIR /app

# TODO(https://github.com/googleapis/librarian/issues/904): Install protoc for gencode.
# TODO(https://github.com/googleapis/librarian/issues/907): Install Python dependencies from requirements.in.
# TODO(https://github.com/googleapis/librarian/issues/905): Install Synthtool by cloning its repo.
# TODO(https://github.com/googleapis/librarian/issues/906): Clone googleapis and run bazelisk build.

# --- Final Stage ---
# This stage creates the lightweight final image, copying only the
# necessary artifacts from the builder stage.
FROM marketplace.gcr.io/google/ubuntu2404

# Install only the essential runtime libraries for Python.
# These are the non "-dev" versions of the libraries used in the builder.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    libssl3 \
    zlib1g \
    libbz2-1.0 \
    libffi8 \
    libsqlite3-0 \
    libreadline8 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# TODO(https://github.com/googleapis/librarian/issues/902): Create a dedicate non-root user and
# switch to the non-root user to run subsequent commands.
# Example:
# RUN groupadd --system --gid 1000 appgroup && \
#     useradd --system --uid 1000 --gid appgroup appuser
# USER appuser

# Copy all Python interpreters, their pip executables, and their standard libraries from the builder.
COPY --from=builder /usr/local/bin/python3.9 /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.9 /usr/local/lib/python3.9

COPY --from=builder /usr/local/bin/python3.10 /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10

COPY --from=builder /usr/local/bin/python3.11 /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11

COPY --from=builder /usr/local/bin/python3.12 /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12

COPY --from=builder /usr/local/bin/python3.13 /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13

# Set the working directory in the container.
WORKDIR /app

# Copy the CLI script into the container.
COPY .generator/cli.py .

# Set the entrypoint for the container to run the script.
ENTRYPOINT ["python3.11", "./cli.py"]
FROM debian:buster-slim

ENV SIGNAL_CLI_VERSION=0.7.4
RUN mkdir -p /usr/share/man/man1 && \
    apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        default-jre-headless \
        curl && \
    pip3 install flask gunicorn && \
    curl -sLo signal-cli-"${SIGNAL_CLI_VERSION}".tar.gz https://github.com/AsamK/signal-cli/releases/download/v"${SIGNAL_CLI_VERSION}"/signal-cli-"${SIGNAL_CLI_VERSION}".tar.gz && \
    tar xf signal-cli-"${SIGNAL_CLI_VERSION}".tar.gz -C /opt && \
    ln -sf /opt/signal-cli-"${SIGNAL_CLI_VERSION}"/bin/signal-cli /usr/local/bin/ && \
    rm signal-cli-"${SIGNAL_CLI_VERSION}".tar.gz && \
    apt-get remove -y python3-pip curl && \
    rm -rf /var/lib/apt/lists/*
ADD server.py .

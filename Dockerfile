FROM ubuntu:20.10

LABEL maintainer="jpdamas15@gmail.com"
LABEL description="Ubuntu 20.10 image ready to execute automatic AOCO sub-routine code correction tool"
LABEL version="1.1"

# Dependencies directory (system wide and Python requirements.txt)
COPY dependencies /dependencies

# Tool source code
COPY src /src

# Ensure packages are up to date
RUN apt-get update

# Install system dependencies
RUN sh /dependencies/install_system_packages.sh

# Install Python dependencies
RUN pip3 install -U -r /dependencies/requirements.txt

# Create alias for tool
RUN echo 'alias code-correction="python3 /src/main.py"' >> ~/.bashrc

# Default command
CMD /bin/bash

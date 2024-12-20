FROM amazonlinux:2

# Install required tools and libraries for building Python from source
RUN yum update -y && \
    yum groupinstall -y "Development Tools" && \
    yum install -y gcc gcc-c++ make wget zlib-devel bzip2 bzip2-devel \
    readline-devel sqlite sqlite-devel openssl-devel xz xz-devel git libffi-devel

# Download and build Python 3.11
RUN cd /usr/src && \
    wget https://www.python.org/ftp/python/3.11.5/Python-3.11.5.tgz && \
    tar xzf Python-3.11.5.tgz && \
    cd Python-3.11.5 && \
    ./configure --enable-optimizations --with-ssl && \
    make altinstall

# Verify Python 3.11 installation
RUN python3.11 --version

# Install pip for Python 3.11 explicitly
RUN python3.11 -m ensurepip --upgrade && \
    python3.11 -m pip install --no-cache-dir --upgrade pip

# Install AWS CLI
RUN python3.11 -m pip install awscli


# Install pip for Python 3.11 explicitly
RUN python3.11 -m ensurepip --upgrade && \
    python3.11 -m pip install --no-cache-dir --upgrade pip


# Install AWS CLI
RUN python3.11 -m pip install awscli

# Install AWS SAM CLI
RUN curl -Lo /tmp/aws-sam-cli.zip https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip && \
    unzip /tmp/aws-sam-cli.zip -d /usr/local/bin/ && \
    rm /tmp/aws-sam-cli.zip

# Copy the requirements.txt into the container
COPY wllm-min-requirements.txt /app/

# Install Python dependencies listed in requirements.txt
RUN pip install -r /app/wllm-min-requirements.txt

# Copy the Lambda function code into the container
COPY hello_world/ /var/task/

# Set the Lambda function handler (entry point)
CMD ["Lambda.lambda_handler"]

# Use the official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.10

# Set working directory
WORKDIR /var/task

# Install system packages
RUN yum install -y \
    git \
    curl \
    && yum clean all

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Set the Lambda function handlers
CMD ["main.lambda_handler"]

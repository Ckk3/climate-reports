FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Conda
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y curl \
    && curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh \
    && bash miniconda.sh -b -p /opt/conda \
    && rm miniconda.sh


ENV PATH="/opt/conda/bin:${PATH}"

WORKDIR /app

# Install dependencies
COPY environment.yml .
RUN conda env create -f environment.yml -n climate_env

# Activate the environment and set it as the default
SHELL ["conda", "run", "-n", "climate_env", "/bin/bash", "-c"]

# Copy the rest of the application code
COPY . .

# Set the command to run your main.py file
CMD ["conda", "run", "-n", "climate_env", "python", "climate_reports_generator/main.py"]

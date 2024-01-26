FROM ghcr.io/ai-dock/jupyter-pytorch:2.1.1-py3.11-cuda-11.8.0-cudnn8-devel-22.04
# image provided by AI-Dock (https://github.com/AI-Dock/jupyter-pytorch)

COPY . /cognos/
WORKDIR /cognos

# Run package installation with root permissions
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip && \
    python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt
# DEBIAN_FRONTEND=noninteractive environment variable is set to prevent interactive prompts during package installations.

ENTRYPOINT ["jupyter", "notebook", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root"]
# docker run --name cognos -it -d -p 8080:80 cognos:latest

# docker run -d -p 8888:8888 jpt:latest
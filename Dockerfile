FROM python:3.9-buster
LABEL version="3.9"
LABEL description="teppanの実行環境"

WORKDIR /work
COPY ./requirements.txt requirements.txt
RUN apt-get update
RUN pip install -r requirements.txt

# install pytorch
RUN pip install torch==1.10.1+cpu torchvision==0.11.2+cpu torchaudio==0.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

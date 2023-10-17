FROM python:3.10-bullseye

RUN apt-get update
RUN apt-get install tesseract-ocr -y
RUN apt-get install tesseract-ocr-rus -y
RUN apt-get install ffmpeg libsm6 libxext6  -y

ADD ../requirements/requirements_bot.txt .
RUN pip install -r ./requirements_bot.txt

COPY .. ./
WORKDIR ./src
CMD python main.py
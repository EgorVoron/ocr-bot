FROM python:3.10-bullseye


ADD ../requirements/requirements_promotion_alert.txt .
RUN pip install -r ./requirements_promotion_alert.txt

COPY .. ./
WORKDIR ./src
CMD python promotion_alert_script.py
FROM python:3.12-bookworm

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY iw_maradeurs_map ./iw_maradeurs_map

ENV BIND=0.0.0.0:3042

CMD [ "python", "-m", "iw_maradeurs_map" ]
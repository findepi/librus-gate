FROM python:3

COPY *py requirements.txt /

RUN set -xeu && \
    pip install --no-cache-dir -r /requirements.txt && \
#    pip install --no-cache-dir \
#        && \
    echo OK

EXPOSE 8723
CMD ["gunicorn", "--bind", "0.0.0.0:8723", "main:app"]

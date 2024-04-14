FROM python:alpine
RUN pip install --upgrade pip

RUN adduser -D nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app
WORKDIR /home/app
USER nonroot

COPY --chown=nonroot:nonroot requirements.txt requirements.txt

# venv
ENV VIRTUAL_ENV=/home/app/venv

# python setup
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN export FLASK_APP=__init__.py
RUN pip install -r requirements.txt

COPY --chown=nonroot:nonroot flaskr flaskr

ENTRYPOINT ["gunicorn"]
CMD [ "-w", "4", "flaskr:app", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-"]
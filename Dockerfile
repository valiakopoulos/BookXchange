#FROM gcr.io/google_appengine/python
FROM us.gcr.io/bookxchange-cs595/appengine/default.v1:main
#LABEL python_version=python
#RUN virtualenv /env -p python

# Install system packages for onelogin dependencies not already included in runtime
#RUN apt-get update && apt-get --yes --quiet install python2.7-dev libxmlsec1-dev nano

# Set virtualenv environment variables. This is equivalent to running
# source /env/bin/activate
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/
CMD gunicorn -c gunicorn.conf.py index:app
FROM python

# Copy the project requirements.txt file to a new folder /app/requirements.txt
COPY requirements.txt /app/requirements.txt

# Configure server here we run commands
RUN set -ex \
    # Runs pip commands and gets latest version of pip...
    && pip install --upgrade pip \
    # Install all from project requirements.txt to application requirements.txt
    && pip install --no-cache-dir -r /app/requirements.txt

# Go to Working Directory
WORKDIR /app

# Here we copy or add project to container app working dir...
ADD . .

#====Defining connection port====
#EXPOSE 8000

##====Running docker locally====
#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "ascons.wsgi:application"]

#====Running docker on heroku====
CMD gunicorn ascons.wsgi:application --bind 0.0.0.0:$PORT

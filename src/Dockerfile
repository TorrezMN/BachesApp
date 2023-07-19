FROM python:3.9

ENV PYTHONUNBUFFERED=1


RUN pip install --upgrade pip

RUN apt-get update 


RUN apt-get install libpq-dev -y 

RUN apt-get install build-essential -y


# ====================



# Add unstable repo to allow us to access latest GDAL builds
# Existing binutils causes a dependency conflict, correct version will be installed when GDAL gets intalled
RUN echo deb http://deb.debian.org/debian testing main contrib non-free >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get remove -y binutils && \
    apt-get autoremove -y

# Install GDAL dependencies
RUN apt-get install -y libgdal-dev g++ --no-install-recommends && \
    pip install pipenv && \
    pip install whitenoise && \
    pip install gunicorn && \
    apt-get clean -y

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ENV LC_ALL="C.UTF-8"
ENV LC_CTYPE="C.UTF-8"


# ====================

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

COPY ./entry.sh /

ENTRYPOINT ["sh", "/entry.sh"]





















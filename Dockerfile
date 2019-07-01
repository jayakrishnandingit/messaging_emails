FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r /code/requirements.txt

COPY logging.yaml /code/logging.yaml
COPY logging_setup.py /code/logging_setup.py
COPY pika_client/ /code/pika_client/

# Copy the current directory contents into the container at /code/
COPY . /code/
# Set the working directory to /code/
WORKDIR /code/

RUN useradd jay
RUN chown -R jay /code
USER jay

CMD exec python emails.py

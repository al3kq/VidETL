# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

RUN apt-get -y update && \
    apt-get install -y ffmpeg \
    rm -rf /var/lib/apt/lists/*


COPY requirements2.txt ./
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements2.txt


# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

RUN mkdir output
# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV MODULE_NAME="api.main"
ENV VARIABLE_NAME="app"
ENV PORT=8000

# Run hypercorn when the container launches
CMD hypercorn $MODULE_NAME:$VARIABLE_NAME --reload --bind 0.0.0.0:$PORT

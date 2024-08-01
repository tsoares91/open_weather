FROM python:3.12.4-slim

# Install requirements 
RUN pip install pandas==2.2.2
RUN pip install requests==2.32.3
RUN pip install mock==5.0.2

# Create the directory and copy the files
WORKDIR /open_weather
COPY . /open_weather

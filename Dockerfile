FROM python:3.7.3-stretch

WORKDIR /

# The enviroment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY . app.py /app/

EXPOSE 8080

# Install packages from requirements.txt
RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt

CMD streamlit run --server.port 8080 --server.enableCORS false app.py

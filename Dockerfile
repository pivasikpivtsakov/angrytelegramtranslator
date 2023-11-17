FROM python:3.11

# create workdir
RUN mkdir /angrytelegramtranslator

# set workdir
WORKDIR /angrytelegramtranslator

# install requirements.txt separately
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy all files
COPY . .

# actual run command
CMD [
        "uvicorn", "main:app",
        "--app-dir", "src/",
        "--host", "0.0.0.0", "--port", "8000"
]

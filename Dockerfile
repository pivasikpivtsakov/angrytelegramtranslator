FROM python:3.11.6-slim

# create workdir
RUN mkdir /angrytelegramtranslator

# set workdir
WORKDIR /angrytelegramtranslator

# install requirements.txt separately
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy all files
COPY . .

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s \
   CMD curl --fail 0.0.0.0:8000/ || exit 1

# actual run command
CMD ["uvicorn", "main:app", "--app-dir", "src/", "--host", "0.0.0.0", "--port", "8000"]

FROM python@sha256:fd76ade0c607f27677bc04be3c60749f400eedc941d9e72967e19a4cedff80c2
WORKDIR /w
COPY requirements.txt .
RUN pip --version
RUN pip install --no-cache-dir -r requirements.txt

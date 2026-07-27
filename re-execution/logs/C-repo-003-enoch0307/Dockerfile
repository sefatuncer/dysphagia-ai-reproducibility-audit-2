# enoch0307/streamlitapp_cn — clean CPU container, AS-DECLARED environment.
# requirements.txt sürüm-sabitlemesiz → box-out re-execution testi (Docker).
FROM python:3.11-slim
WORKDIR /app
COPY repo/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY repo/ /app/repo/
COPY rerun_test.py /app/rerun_test.py
CMD ["python", "rerun_test.py"]

FROM python:3.12.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "python", "combined_script.py" ]

#TASK: Update this repo or create a new one to use the calculator app from earlier to output 2*32
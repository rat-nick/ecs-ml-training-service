FROM python:3.8-slim
COPY server app
WORKDIR /app
RUN rm -rf env
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "api.py" ]
EXPOSE 5000
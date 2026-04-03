FROM python:3.10-slim
WORKDIR /app
COPY file.py .
CMD ["sh", "-c", "python3 file.py && tail -f /dev/null"]                                                                                                                                       

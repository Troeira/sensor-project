FROM python:3.9
# Or any preferred Python version.
COPY tp2_data_publisher_base.py ./main.py
RUN pip install paho-mqtt numpy
CMD ["python", "./main.py"] 
# Or enter the name of your unique directory and parameter set.
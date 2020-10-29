FROM python:3.8
WORKDIR /app

COPY requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y locales
RUN locale-gen ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

COPY ./src /app
RUN alembic init alembic
RUN mv -f /app/models/alembic.ini /app/alembic.ini
RUN mv -f /app/models/env.py /app/alembic/env.py
CMD ["python","app.py"]
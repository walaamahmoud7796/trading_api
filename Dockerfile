FROM python:3-onbuild
COPY . /usr/src/app
CMD ["python","thndr/db.py"]
CMD ["python","run.py"]
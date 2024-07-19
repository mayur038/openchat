python3 -m pip install -r requirements.txt && python3 manage.py collectstatic --noinput && pip3 install pysqlite3 && python3 manage.py migrate

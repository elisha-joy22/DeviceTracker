pip install -r requirements.txt

python manage.py migrate
python manage.py makemigrations accounts
python manage.py makemigrations assign
python manage.py makemigrations device
python manage.py migrate
python manage.py run_startup_functions
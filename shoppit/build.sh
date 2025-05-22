

set -o errexit #exit on error

pip install -r requirement.txt

python manage.py collectstatic --no-input
python manage.py migrate
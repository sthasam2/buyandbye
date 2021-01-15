.zsh
VENV=".venv"

echo "Setup BuyandBye"
echo "---------------"
echo "requirements: Python3, Pip, Virtualenv"
echo " "

if [-d "$VENV"]; then
    echo "Creating virtual environment in folder .venv"
    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
fi

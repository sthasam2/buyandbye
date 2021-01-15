CURR=`pwd`
VENV=".venv/"

echo "\e[1;92mSetup BuyandBye\e[0m"
echo "---------------"
echo "requirements: Python3, Pip, Virtualenv"
echo " "

if [ -d "$CURR/$VENV" ]; then
    echo "Requirements satisfied!"
else
    echo "Creating virtual environment in folder \e[1m.venv\e[0m..."
    virtualenv .venv
    
    echo "Installing Requirements...\n"
    ./.venv/bin/pip install -r requirements.txt
    ./.venv/bin/python manage.py makemigrations
    ./.venv/bin/python manage.py migrate
fi

# activate() {. .venv/bin/activate}
# echo "Hello"



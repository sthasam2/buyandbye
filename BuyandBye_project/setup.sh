CURR=`pwd`
VENV=".venv/"

echo "---------------"
echo "\e[1;92mBuyandBye Setup\e[0m"
echo "---------------\n"

echo "\e[1;4mREQUIREMENTS:\e[0m\n1. Python3 \n2. Pip \n3. Virtualenv"
echo " "

if [ -d "$CURR/$VENV" ]; then
    echo "Virtual environment already available!"
else
    echo "Creating virtual environment in folder \e[1m.venv\e[0m...\n"
    virtualenv .venv
    
    echo "\n\e[1;92mInstalling Dependencies...\e[0m\n"
    ./.venv/bin/pip install -r requirements.txt
    echo " "
    ./.venv/bin/python manage.py makemigrations    
    echo " "
    ./.venv/bin/python manage.py migrate    
fi

echo "\e[1;92mSETUP COMPLETE!"



Write-Host "Setup BuyandBye"
Write-Host "---------------"
Write-Host "requirements: Python3, Pip, Virtualenv"
Write-Host " "

$VENV=".venv"
if (-not (Test-Path -LiteralPath $VENV)){
    try {
        python3 -m pip install --user Virtualenv
        virtualenv venv
    }
    catch{
        Write-Error -Message "Unable to create virtual environment"
    }
}
else{
    "Virtual environment already installed"
}

./venv/scripts/activate
pip install -r requirements.txt
python manage.py createmigrations
python manage.py migrate

Write-Host "Setup Complete"
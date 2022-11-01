mkdir package
pip3 install --target ./package -r requirements.txt
cd package
zip -r crime-stats.zip .
cd ..
pip3 freeze --path ./package > requirements.txt
zip -g package/crime-stats.zip index.py
zipinfo package/crime-stats.zip
terraform plan
mkdir package
touch package/hello-python.zip
pip3 install --target ./package -r requirements.txt
cd package
zip -r hello-python.zip .
cd ..
pip3 freeze --path ./package > requirements.txt
zip -g package/hello-python.zip index.py
zipinfo package/hello-python.zip
terraform plan -refresh-only
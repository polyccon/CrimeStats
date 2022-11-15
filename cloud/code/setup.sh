mkdir package
pip3 install --target ./package -r requirements.txt
cd package
zip -r crime-stats.zip .
cd ..
pip3 freeze --path ./package > requirements.txt
zip -g zip/crime-stats.zip index.py
zipinfo zip/crime-stats.zip
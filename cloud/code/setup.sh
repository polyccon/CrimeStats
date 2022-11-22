mkdir package zip
pip3 install --target ./package -r requirements.txt
cd package
zip -r crime-stats.zip .
cd ..
mv package/crime-stats.zip zip/crime-stats.zip
pip3 freeze --path ./package > requirements.txt
zip -g zip/crime-stats.zip index.py
zipinfo zip/crime-stats.zip
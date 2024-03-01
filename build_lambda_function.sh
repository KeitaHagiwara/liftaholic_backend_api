pip install -t ./python_packages -r requirements.txt
cd ./python_packages
zip ../aws_lambda_function.zip -r .
cd ..

zip aws_lambda_function.zip -u main.py
zip aws_lambda_function.zip -u -r api
zip aws_lambda_function.zip -u -r config
zip aws_lambda_function.zip -u -r crud
zip aws_lambda_function.zip -u -r db
zip aws_lambda_function.zip -u -r migrations

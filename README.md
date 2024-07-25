Comands:


run all the commands on /climate-reports

# Up TCP server
python climate_reports_generator/main.py


# Generate pdf
python climate_reports_generator/report_generator.py 01234567891,78945612348 2024-01-01T00:00 climate_reports_generator/raw_data/test_data.txt --ENVIA_EMAIL


# Run tests and create sample data
pytest climate_reports_generator/tests.py


# Testing
You can send the email using a smtp service (I used https://mailtrap.io/email-sending/, with the free plan you can send to the email you use to create the account), and the program will send to the user email.

The code will send a email with the report 

## example image sended with the report on anexo
![alt text](image.png)
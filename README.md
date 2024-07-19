Comands:


run all the commands on /climate-reports

# Up TCP server
python climate_reports_generator/tcpserver.py


# Generate pdf
python climate_reports_generator/report_generator.py 01234567891,78945612348 2024-01-01T00:00 climate_reports_generator/raw_data/test_data.txt --ENVIA_EMAIL


# Run tests
pytest climate_reports_generator/tests.py

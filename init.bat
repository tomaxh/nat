@echo off
type setup/up.sql | psql --username=postgres
python setup/load_cats.py
python setup/transfer_nat.py data/new.csv
python setup/updateCats.py
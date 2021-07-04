all: install-env install-dep clean quality run deploy-dash
PIP := pip
POETRY := poetry
LUDWIG :=lugwig

install-env:
		${PIP} install -U poetry

install-dep:
		@echo 'Installing dependencies'
		${POETRY} install

tests:
		@echo 'Running test'
		${POETRY} run pytest testsg

clean:
		@echo 'Removing python self generated unwanted files'
		find . -name '__pycache__' -exec rm -fr {} +
		find . -name '*pyo' -exec rm -f {} +
		find . -name '*pyc' -exec rm -f {} +
		find . -name 'ipynb_checkpoints' -exec rn -rf {} +
		find . -name '.DS_Store' -exec rm -rf {} +

quality:
		@echo 'check for linting, Typing, code formating, safety'
		${POETRY} run tox -e py

data-prep:
		${POETRY} run data_prep.py

train: 
		${LUDWIG} experiment --dataset s3://ml-artifact-store/data/filtered.csv --config_file train.yaml --output_directory s3://ml-artifact-store/model  --experiment_name experiemnt_run_1 --model_name covid_classifier

deploy:
		${POETRY} run streamlit run main.py &

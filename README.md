# Trainslator

## Overview

This application aims at providing a Google Translate like application for enterprise use. The goal is to make sure corporate data remains within the GCP environment of the company and is not shared with Google.

## Release Notes

### Version 0.1

- Translate text from typed input (EN to FR)

### Version 0.2

- Translate PDF documents (EN to FR)

### Version 0.3

- Made UI nicer

### Version 0.4

- Add glossary option

### Version 0.5

- Improve glossary look

### Version 0.6

- FR to EN translation

## Build and deploy

### Create Glossary

- Update the `/glossary/glossary.csv` with your terms
- Update the variables at the top of the `/glossary/create-glossary.py` file
- Run the `/glossary/local-prereqs.sh` script
- Run the `/glossary/create-glossary.sh` script

### Run the app locally

- First, run the `/app/local-prereqs.sh` script
- Run the `/app/local-run.sh`
- Browse to `localhost:8082`

### Deploy app to Cloud Run

- Update and run the `/app/build.sh` script
- Update and run the `/app/deploy.sh` script
- Update the `/infra/providers.tf` and `/infra/variables` files with proper values
- Run `terraform init` and `terraform apply` from the `/infra` directory

## References

- [Translating Text (Advanced)](https://cloud.google.com/translate/docs/advanced/translating-text-v3)
- [Translate Documents](https://cloud.google.com/translate/docs/advanced/translate-documents)
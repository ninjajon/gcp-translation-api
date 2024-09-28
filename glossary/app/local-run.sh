python3 -m venv app-streamlit
source app-streamlit/bin/activate

export GCP_PROJECT="jo-trainslator-antl"
export GCP_REGION="us-central1"

#gcloud auth application-default login
gcloud config set project $GCP_PROJECT
gcloud config set compute/region $GCP_REGION

streamlit run glossary.py \
  --browser.serverAddress=localhost \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false \
  --server.port 8083
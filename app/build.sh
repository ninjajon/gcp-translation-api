export GCP_PROJECT="jo-trainslator-antl"
export GCP_REGION="us-central1"
export AR_REPO="trainslator-repo"
export SERVICE_NAME="trainslator"

#make sure you are in the active directory for "gemini-streamlit-cloudrun"
gcloud config set project $GCP_PROJECT
gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repository-format=Docker
gcloud auth configure-docker "$GCP_REGION-docker.pkg.dev"
gcloud builds submit --tag "$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME"

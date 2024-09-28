export GCP_PROJECT="jo-trainslator-antl"
export GCP_REGION="us-central1"
export AR_REPO="trainslator-repo"
export SERVICE_NAME="trainslator-glossary"
export DEFAULT_COMPUTE_SERVICE_ACCOUNT="589130920841-compute@developer.gserviceaccount.com"

gcloud projects add-iam-policy-binding $GCP_PROJECT \
  --member="serviceAccount:$DEFAULT_COMPUTE_SERVICE_ACCOUNT" \
  --role="roles/logging.logWriter"

gcloud projects add-iam-policy-binding $GCP_PROJECT \
  --member="serviceAccount:$DEFAULT_COMPUTE_SERVICE_ACCOUNT" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $GCP_PROJECT \
  --member="serviceAccount:$DEFAULT_COMPUTE_SERVICE_ACCOUNT" \
  --role="roles/artifactregistry.writer"

gcloud config set project $GCP_PROJECT
gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repository-format=Docker
gcloud auth configure-docker "$GCP_REGION-docker.pkg.dev"
gcloud builds submit --tag "$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME"

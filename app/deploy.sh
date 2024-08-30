export GCP_PROJECT="jo-trainslator-antl"
export GCP_REGION="us-central1"
export AR_REPO="trainslator-repo"
export SERVICE_NAME="trainslator"

gcloud config set project $GCP_PROJECT

gcloud iam service-accounts create "$SERVICE_NAME"

gcloud projects add-iam-policy-binding $GCP_PROJECT \
  --member="serviceAccount:$SERVICE_NAME@$GCP_PROJECT.iam.gserviceaccount.com" \
  --role="roles/cloudtranslate.user"

gcloud projects add-iam-policy-binding $GCP_PROJECT \
  --member="serviceAccount:$SERVICE_NAME@$GCP_PROJECT.iam.gserviceaccount.com" \
  --role="roles/logging.logWriter"

gcloud projects add-iam-policy-binding $GCP_PROJECT \
  --member="serviceAccount:$SERVICE_NAME@$GCP_PROJECT.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $GCP_PROJECT \
  --member="serviceAccount:$SERVICE_NAME@$GCP_PROJECT.iam.gserviceaccount.com" \
  --role="roles/cloudtrace.agent"

gcloud run deploy "$SERVICE_NAME" \
  --port=8080 \
  --image="$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME" \
  --allow-unauthenticated \
  --region=$GCP_REGION \
  --platform=managed  \
  --project=$GCP_PROJECT \
  --service-account="$SERVICE_NAME" \
  --ingress=internal-and-cloud-load-balancing



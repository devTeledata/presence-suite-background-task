help:
	@echo "Local examples:"
	@echo "    make run-dev       # Starts a FastAPI development server locally."
	@echo "    make install       # install requirements.txt."

install:
	pip install -r requirements.txt

run-dev:
	export GOOGLE_APPLICATION_CREDENTIALS=credentials/cred.json && \
	export DEV=true && \
	uvicorn main:app --port 8080 --reload

deploy-tivit:
	gcloud config configurations activate sulamerica && \
	gcloud builds submit --config=cloudbuild_chat_saude.yaml --gcs-source-staging-dir=gs://us.artifacts.sas-enduser-chat-saude.appspot.com/images

deploy-mega:
	gcloud config configurations activate sulamerica-mega && \
	gcloud builds submit --config=cloudbuild.yaml --gcs-source-staging-dir=gs://artifacts.sas-enduser-chat-ti.appspot.com/images

deploy-santo:
	gcloud config configurations activate default && \
	gcloud builds submit --config=cloudbuild_dev.yaml

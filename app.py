from flask import Flask, request, jsonify
from minio import Minio
import io
import os
import uuid

app = Flask(__name__)

# Configure MinIO client using environment variables
minio_client = Minio(
    os.environ.get("MINIO_ENDPOINT", "minio.example.com"),
    access_key=os.environ.get("MINIO_ACCESS_KEY", "your-access-key"),
    secret_key=os.environ.get("MINIO_SECRET_KEY", "your-secret-key"),
    secure=True
)

BUCKET_NAME = os.environ.get("MINIO_BUCKET", "webhook-data")

# Ensure bucket exists
if not minio_client.bucket_exists(BUCKET_NAME):
    minio_client.make_bucket(BUCKET_NAME)

@app.route("/webhook", methods=["POST"])
def receive_webhook():
    try:
        payload = request.data
        filename = f"{uuid.uuid4()}.json"

        minio_client.put_object(
            BUCKET_NAME,
            filename,
            io.BytesIO(payload),
            length=len(payload),
            content_type="application/json"
        )

        return jsonify({"status": "success", "filename": filename}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

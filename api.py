from flask import Flask, request, jsonify
import boto3
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# AWS S3 configuration
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')
S3_BASE_URL = f'https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/'

# Initialize S3 client using the "wallex-sentinel" profile
session = boto3.Session(profile_name='wallex-sentinel')
s3_client = session.client('s3', region_name=AWS_REGION)

@app.route('/' , methods=['GET'])
def index():
    response = s3_client.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]
    return jsonify(bucket_names)
    # return 'Hello, World!'

@app.route('/get-image', methods=['GET'])
def get_image():
    params = request.args.to_dict()
    
    # List all objects in the specified bucket
    response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
    
    if 'Contents' in response:
        # Get all the object keys (names)
        image_names = [obj['Key'] for obj in response['Contents']]
    else:
        image_names = []

    # Specific image key
    image_key = '1_acra.pdf'
    image_url = f'{S3_BASE_URL}{image_key}'
    
    params['image_url'] = image_url
    params['image_names'] = image_names
    
    return jsonify(params)

@app.route('/save-image', methods=['POST'])
def post_body():
    data = request.get_json()
    placeholder_image_path = 'placeholder.jpg'
    if os.path.exists(placeholder_image_path):
        s3_key = 'uploaded/placeholder.jpg' 
        with open(placeholder_image_path, 'rb') as image_file:
            s3_client.upload_fileobj(image_file, AWS_BUCKET_NAME, s3_key)
        uploaded_image_url = f'{S3_BASE_URL}{s3_key}'
        data['uploaded_image_url'] = uploaded_image_url
    else:
        data['error'] = 'Placeholder image not found'
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
import os
import requests
import json

class DatasetDownloader:
    def __init__(self, credentials_file, api_url, destination_folder):
        self.credentials_file = credentials_file
        self.api_url = api_url
        self.destination_folder = destination_folder

    def download_dataset(self):
        # Read Kaggle credentials
        with open(self.credentials_file, 'r') as file:
            kaggle_credentials = json.load(file)

        headers = {
            'Authorization': f"Bearer {kaggle_credentials['key']}"
        }
        
        response = requests.get(self.api_url, headers=headers, stream=True)
        response.raise_for_status()  # Raise an error for failed request

        dataset_zip = os.path.join(self.destination_folder, 'dataset.zip')
        with open(dataset_zip, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Unzip the dataset
        import zipfile
        with zipfile.ZipFile(dataset_zip, 'r') as zip_ref:
            zip_ref.extractall(self.destination_folder)

        print("Dataset downloaded and extracted.")

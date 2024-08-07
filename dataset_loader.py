import os
import requests
import json
import zipfile

class DatasetDownloader:
    def __init__(self, credentials_file, api_url, destination_folder):
        """
        Initialize the DatasetDownloader with necessary parameters.

        :param credentials_file: Path to the file containing Kaggle API credentials (in JSON format).
        :param api_url: URL of the Kaggle API endpoint to download the dataset from.
        :param destination_folder: Directory where the dataset will be saved and extracted.
        """
        self.credentials_file = credentials_file
        self.api_url = api_url
        self.destination_folder = destination_folder

    # Shouldn't this be an async-method, as it is trying to download data?
    def download_dataset(self):
        """
        Download the dataset from Kaggle and extract it into the destination folder.

        This method reads Kaggle API credentials, sends a request to the API to download the dataset,
        saves the dataset to a zip file, and then extracts the contents of the zip file.
        """
        # **Single Responsibility Principle (SRP):**
        # The class is responsible solely for downloading and extracting datasets.
        # This method handles everything related to dataset downloading and extraction,
        # adhering to SRP by not mixing in other responsibilities.

        # reading the Kaggle credentials from the provided file
        with open(self.credentials_file, 'r') as file:
            kaggle_credentials = json.load(file)

        headers = {
            'Authorization': f"Bearer {kaggle_credentials['key']}"
        }
        
        # **Encapsulation:**
        # The class encapsulates the details of making the API request,
        # handling the response, saving the zip file, and extracting it.
        # Users of the class interact with a high-level method without needing to know these details.

        # Send a request to download the dataset
        response = requests.get(self.api_url, headers=headers, stream=True)
        response.raise_for_status()  # Raise an error if the request failed

        # Define the path to save the downloaded dataset
        dataset_zip = os.path.join(self.destination_folder, 'dataset.zip')
        
        # Save the dataset to a zip file
        with open(dataset_zip, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # **Error Handling:**
        # Proper error handling is done with `response.raise_for_status()` to ensure that
        # any issues with the request are caught early, preventing further processing
        # of an invalid response.

        # Unzip the downloaded dataset
        with zipfile.ZipFile(dataset_zip, 'r') as zip_ref:
            zip_ref.extractall(self.destination_folder)

        # **Readability and Maintainability:**
        # Clear comments and structured code help maintain readability and make future modifications
        # easier. Each part of the code has a clear purpose and is easy to follow.

        print("Dataset downloaded and extracted.")

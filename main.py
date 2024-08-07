import os
import logging
from dataset_loader import DatasetDownloader
from pipeline_model import ModelPipeline
from production_pipeline import ProductionPipeline

def setup_logging():
    """
    Set up logging configuration for the application.

    Configures the logging to output messages to the console with a specific format.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler()])
    logging.info("Logging setup complete.")

def main():
    """
    Main function to execute the data pipeline, including dataset download, model training, 
    and production pipeline monitoring.

    Steps:
    1. Setup logging configuration.
    2. Define file paths and URLs for dataset and model.
    3. Download the dataset.
    4. Verify the dataset file exists.
    5. Initialize and run the model pipeline if the model file is found.
    6. Initialize and run the production pipeline if the configuration file is found.
    """
    # Setup logging configuration
    setup_logging()

    # Defining paths and URLs
    credentials_file = 'C:/Users/mozhdeh/Desktop/programming 4/kaggle.json'
    api_url = 'https://www.kaggle.com/api/v1/datasets/download/nphantawee/pump-sensor-data'
    destination_folder = 'output'
    dataset_file_name = 'sensor.csv'
    dataset_path = os.path.join(destination_folder, dataset_file_name)
    model_path = os.path.join(destination_folder, 'model.joblib')
    config_path = 'application.json'

    # Creating destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Initializing and using the ModelPipeline module
    # I don't understand this: You seem to be making a model, but only if it already exists?
    # Neither do I get the difference between the ModelPipeLine and the ProductionPipeLine.
    if os.path.isfile(model_path):
        try:
            model_pipeline = ModelPipeline(model_path=model_path, data_dir=destination_folder)
            logging.info("Found model file. Running model pipeline...")
            model_pipeline.run_pipeline(input_data_path=dataset_path)
            logging.info("Model pipeline execution completed.")
        except Exception as e:
            logging.error("An error occurred during model pipeline execution: %s", e)
            return
    else:
        logging.error("Model file not found at %s", model_path)
        return

    # Initialize and run the production pipeline module
    if os.path.isfile(config_path):
        try:
            logging.info("Starting production pipeline...")
            production_pipeline = ProductionPipeline(config_path=config_path)
            
            # Start monitoring the input directory for new files
            production_pipeline.start_monitoring()
            logging.info("Production pipeline is now monitoring for new files.")
        except Exception as e:
            logging.error("An error occurred while running the production pipeline: %s", e)
    else:
        logging.error("Configuration file not found at %s", config_path)

if __name__ == "__main__":
    main()

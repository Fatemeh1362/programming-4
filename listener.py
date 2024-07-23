import os
import pandas as pd
import json
import logging
from predictor import Predictor
from utils import plot_sensor_anomalies, save_plot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_data(df):
    for col in df.select_dtypes(include=['datetime64']):
        df[col] = df[col].astype(int) / 10**9  # Convert to Unix timestamp
    return df

class Listener:
    def __init__(self, config):
        self.input_dir = config.get('input_dir', 'C:/Users/mozhdeh/Desktop/programming 4/input')
        self.output_dir = config.get('output_dir', 'C:/Users/mozhdeh/Desktop/programming 4/output')
        self.img_dir = config.get('img_dir', 'C:/Users/mozhdeh/Desktop/programming 4/img')

        # Ensure directories exist
        for directory in [self.input_dir, self.output_dir, self.img_dir]:
            if not os.path.exists(directory):
                logging.info(f"Creating directory: {directory}")
                os.makedirs(directory)

        if not os.path.exists(self.input_dir):
            raise FileNotFoundError(f"Input directory not found: {self.input_dir}")

        self.predictor = Predictor()
        self.model_fitted = False

    def get_files(self):
        files = os.listdir(self.input_dir)
        logging.info(f"Files in input directory: {files}")
        return files

    def fit_model(self):
        logging.info(f"Attempting to fit model with data from {self.input_dir}")
        for filename in self.get_files():
            if filename.startswith('train_') and filename.endswith('.csv'):
                filepath = os.path.join(self.input_dir, filename)
                logging.info(f"Processing training file: {filepath}")
                try:
                    training_data = pd.read_csv(filepath, parse_dates=True)
                    training_data = preprocess_data(training_data)
                    self.predictor.fit(training_data)
                    self.model_fitted = True
                    logging.info("Model fitted with training data.")
                except Exception as e:
                    logging.error(f"Error fitting model: {e}")

    def listen(self, max_files=5):
        self.fit_model()
        logging.info("Listening for new data...")
        files_processed = 0
        for filename in self.get_files():
            if files_processed >= max_files:
                break
            if filename.endswith(".csv") and not filename.startswith('train_'):
                filepath = os.path.join(self.input_dir, filename)
                logging.info(f"Processing file: {filepath}")
                try:
                    new_data = pd.read_csv(filepath, parse_dates=True)
                    new_data = preprocess_data(new_data)
                    if self.model_fitted:
                        predictions = self.predictor.predict(new_data)
                        output_path = os.path.join(self.output_dir, f"predictions_{filename}")
                        pd.DataFrame(predictions).to_csv(output_path)
                        logging.info(f"Predictions saved to {output_path}")
                    files_processed += 1
                except Exception as e:
                    logging.error(f"Error processing file {filename}: {e}")

        logging.info(f"Processed {files_processed} files.")
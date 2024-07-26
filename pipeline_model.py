import os
import joblib
import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

class ModelPipeline:
    def __init__(self, model_path, data_dir):
        self.model_path = model_path
        self.data_dir = data_dir
        self.model = RandomForestClassifier(random_state=42)
        self.train_df = None
        self.val_df = None
        self.test_df = None
        self.X_train = None
        self.y_train = None
        self.X_val = None
        self.y_val = None
        logging.basicConfig(filename='model_pipeline.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def load_data(self, data_path):
        logging.info("Loading data from %s", data_path)
        try:
            df = pd.read_csv(data_path)
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df = df.dropna(subset=['timestamp'])
            df.set_index('timestamp', inplace=True)
            df.drop(columns=['Unnamed: 0'], errors='ignore', inplace=True)

            self.train_df = df.loc['2018-04-01':'2018-06-30']
            self.val_df = df.loc['2018-07-01':'2018-07-31']
            self.test_df = df.loc['2018-08-01':'2018-08-31']

            self.train_df.to_csv(os.path.join(self.data_dir, 'train_data.csv'))
            self.val_df.to_csv(os.path.join(self.data_dir, 'val_data_july.csv'))
            self.test_df.to_csv(os.path.join(self.data_dir, 'test_data_august.csv'))

            logging.info("Data loaded and saved: train_data.csv, val_data_july.csv, test_data_august.csv")
        except Exception as e:
            logging.error(f"Error loading or processing data: {e}")
            raise

    def split_data(self):
        if self.train_df is None:
            raise ValueError("Training data not loaded. Please load the data first.")

        X = self.train_df.drop(columns=['machine_status'])
        y = self.train_df['machine_status']

        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(X, y, test_size=0.3, random_state=42)
        logging.info("Data split into training and validation sets.")

    def train_model(self):
        if self.X_train is None or self.y_train is None:
            raise ValueError("Training data not available. Please split the data first.")

        self.model.fit(self.X_train, self.y_train)
        joblib.dump(self.model, self.model_path)
        logging.info("Model trained and saved to %s", self.model_path)

    def evaluate_model(self):
        if self.X_val is None or self.y_val is None:
            raise ValueError("Validation data not available. Please split the data first.")

        predictions = self.model.predict(self.X_val)
        accuracy = accuracy_score(self.y_val, predictions)
        report = classification_report(self.y_val, predictions, zero_division=0)

        logging.info(f"Validation Accuracy: {accuracy:.2f}")
        logging.info("Classification Report:\n%s", report)
        print(f"Validation Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)

    def plot_sensor_anomalies(self, sensor_name):
        if self.train_df is None:
            raise ValueError("Training data not available. Please load the data first.")

        plot_file = os.path.join(self.data_dir, f'anomaly_plot_{sensor_name}.png')
        plt.figure(figsize=(14, 7))
        sns.lineplot(data=self.train_df, x=self.train_df.index, y=sensor_name, label=sensor_name)
        plt.title(f'Anomaly Detection for {sensor_name}')
        plt.xlabel('Time')
        plt.ylabel('Sensor Value')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(plot_file)
        plt.close()
        logging.info("Anomaly plot saved to %s", plot_file)
        return plot_file

    def process_new_data(self, file_path):
        logging.info("Processing new data from %s", file_path)
        model = joblib.load(self.model_path)
        new_data = pd.read_csv(file_path)

        new_data['timestamp'] = pd.to_datetime(new_data['timestamp'], errors='coerce')
        new_data = new_data.dropna(subset=['timestamp'])
        new_data.set_index('timestamp', inplace=True)
        new_data.drop(columns=['Unnamed: 0'], errors='ignore', inplace=True)

        X_new = new_data.drop(columns=['machine_status'])
        predictions = model.predict(X_new)
        return predictions

    def run_pipeline(self, input_data_path):
        logging.info("Running pipeline")
        self.load_data(input_data_path)
        self.split_data()
        self.train_model()
        self.evaluate_model()

        # Plot anomalies for a specific sensor
        plot_file = self.plot_sensor_anomalies('sensor_01')
        print(f"Anomaly plot saved to {plot_file}")

        # Process new data and make predictions
        predictions = self.process_new_data(os.path.join(self.data_dir, 'test_data_august.csv'))
        print("Predictions for new data:\n", predictions)

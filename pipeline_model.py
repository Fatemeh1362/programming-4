import os
import joblib
import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler

class ModelPipeline:
    """
    A class for managing the machine learning pipeline, including data processing,
    model training, evaluation, and anomaly plotting. This class adheres to SOLID principles
    to ensure modularity, flexibility, and maintainability.
    """

    def __init__(self, model_path, data_dir):
        """
        Initializing the ModelPipeline with paths for the model and data directory.

        :param model_path: Path where the trained model will be saved.
        :param data_dir: Directory where data and log files will be stored.
        """
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
        self.scaler = None
        logging.basicConfig(filename=os.path.join(data_dir, 'model_pipeline.log'), level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def load_data(self, data_path):
        """
        Load and preprocess the data from the specified path.

        :param data_path: Path to the CSV file containing the dataset.
        :raises: Exception if data loading or processing fails.
        :sol: Single Responsibility Principle (SRP)
        :rep: Data loading and preprocessing are handled in this method, encapsulating this functionality.
        """
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
            logging.error("Error loading or processing data: %s", e)
            raise

    def split_data(self):
        """
        Split the training data into training and validation sets.

        :raises: ValueError if training data is not loaded.
        :sol: Single Responsibility Principle (SRP)
        :rep: Data splitting is handled here, ensuring that the method focuses solely on this task.
        """
        if self.train_df is None:
            raise ValueError("Training data not loaded. Please load the data first.")
        X = self.train_df.drop(columns=['machine_status'])
        y = self.train_df['machine_status']
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(X, y, test_size=0.3, random_state=42)
        logging.info("Data split into training and validation sets.")

    def transform_data(self):
        """
        Scale the training data using StandardScaler.

        :raises: ValueError if training data is not available.
        :sol: Single Responsibility Principle (SRP)
        :rep: Data transformation is performed here, which isolates this responsibility from other methods.
        """
        if self.X_train is None:
            raise ValueError("Training data not available. Please load and split the data first.")
        self.scaler = StandardScaler()
        self.X_train = self.scaler.fit_transform(self.X_train)
        logging.info("Data transformation completed.")

    def train_model(self):
        """
        Train the RandomForestClassifier model and save it to the specified path.

        :raises: ValueError if training data is not available.
        :sol: Single Responsibility Principle (SRP)
        :rep: Model training is encapsulated in this method, adhering to the principle of one responsibility per method.
        """
        if self.X_train is None or self.y_train is None:
            raise ValueError("Training data not available. Please load and split the data first.")
        self.model.fit(self.X_train, self.y_train)
        joblib.dump(self.model, self.model_path)
        logging.info("Model trained and saved to %s", self.model_path)

    def evaluate_model(self):
        """
        Evaluate the trained model using validation data and log the results.

        :raises: ValueError if validation data is not available.
        :sol: Single Responsibility Principle (SRP)
        :rep: Evaluation is focused on assessing the model's performance and logging the results.
        """
        if self.X_val is None or self.y_val is None:
            raise ValueError("Validation data not available. Please split the data first.")
        predictions = self.model.predict(self.X_val)
        accuracy = accuracy_score(self.y_val, predictions)
        report = classification_report(self.y_val, predictions, zero_division=0)
        logging.info("Validation Accuracy: %.2f", accuracy)
        logging.info("Classification Report:\n%s", report)
        print("Validation Accuracy: %.2f" % accuracy)
        print("Classification Report:\n", report)

    def plot_sensor_anomalies(self, df, sensor_name):
        """
        Plot sensor anomalies and save the plot as an image file.

        :param df: DataFrame containing sensor data.
        :param sensor_name: Name of the sensor to plot.
        :returns: Path to the saved plot image file.
        :raises: ValueError if data is not available.
        :sol: Single Responsibility Principle (SRP)
        :rep: Plotting sensor anomalies is managed separately from other tasks.
        """
        if df is None:
            raise ValueError("Data not available. Please provide the data.")
        
        plt.figure(figsize=(14, 7))
        sns.lineplot(data=df, x=df.index, y=sensor_name, label=sensor_name)
        plt.title(f'Anomaly Detection for {sensor_name}')
        plt.xlabel('Time')
        plt.ylabel('Sensor Value')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plot_file = os.path.join(self.data_dir, f'anomaly_plot_{sensor_name}.png')
        plt.savefig(plot_file)
        plt.close()
        logging.info("Anomaly plot saved to %s", plot_file)
        
        return plot_file

    def process_new_data(self, file_path):
        """
        Process the new data using the trained model and return predictions.

        :param file_path: Path to the new data CSV file.
        :returns: Predictions for the new data.
        :raises: Exception if processing fails.
        :sol: Single Responsibility Principle (SRP)
        :rep: New data processing is isolated to ensure clarity and ease of management.
        """
        logging.info("Processing new data from %s", file_path)
        try:
            model = joblib.load(self.model_path)
            new_data = pd.read_csv(file_path)
            new_data['timestamp'] = pd.to_datetime(new_data['timestamp'], errors='coerce')
            new_data = new_data.dropna(subset=['timestamp'])
            new_data.set_index('timestamp', inplace=True)
            new_data.drop(columns=['Unnamed: 0'], errors='ignore', inplace=True)
            X_new = new_data.drop(columns=['machine_status'])
            if self.scaler is None:
                raise ValueError("Scaler not available. Please train the model and apply transformation first.")
            X_new = self.scaler.transform(X_new)
            predictions = model.predict(X_new)
            return predictions
        except Exception as e:
            logging.error("Error processing new data: %s", e)
            raise

    def run_pipeline(self, input_data_path):
        """
        Execute the full model pipeline: data loading, splitting, transformation,
        training, evaluation, and anomaly plotting.

        :param input_data_path: Path to the CSV file containing the dataset.
        """
        logging.info("Running pipeline")
        self.load_data(input_data_path)
        self.split_data()
        self.transform_data()
        self.train_model()
        self.evaluate_model()
        
        # Plot anomalies for sensor_04 and sensor_51
        plot_file_04 = self.plot_sensor_anomalies(self.train_df, 'sensor_04')
        plot_file_51 = self.plot_sensor_anomalies(self.train_df, 'sensor_51')
        
        print(f"Anomaly plot for sensor_04 saved to {plot_file_04}")
        print(f"Anomaly plot for sensor_51 saved to {plot_file_51}")
        
        predictions = self.process_new_data(os.path.join(self.data_dir, 'test_data_august.csv'))
        print("Predictions for new data:\n", predictions)
        
# #Single Responsibility Principle (SRP)
# Each method in the ModelPipeline class is responsible for a single part of the functionality:

# load_data: Responsible for loading and preprocessing the data.
# split_data: Handles the splitting of data into training and validation sets.
# transform_data: Takes care of scaling the data.
# train_model: Manages the training of the model and saving it.
# evaluate_model: Evaluates the model using the validation data and logs the results.
# plot_sensor_anomalies: Plots and saves sensor anomaly data.
# process_new_data: Processes new data for predictions.
# run_pipeline: Orchestrates the entire pipeline by calling the other methods in sequence.
# Open/Closed Principle (OCP)
# The class is open for extension but closed for modification. New functionalities can be added by extending the class or adding new methods without changing the existing code.
# Liskov Substitution Principle (LSP)
# Any subclass that extends ModelPipeline can replace it without altering the correctness of the program. For example, a subclass can override load_data to change how data is loaded while keeping the rest of the pipeline intact.
# Interface Segregation Principle (ISP)
# The class methods are highly specific and only perform one task, ensuring that any changes or extensions will not affect unrelated parts of the class.
# Dependency Inversion Principle (DIP)
# The class depends on abstractions (interfaces) rather than concrete implementations. It uses standard libraries (joblib, pandas, logging, matplotlib, seaborn, sklearn) which can be easily replaced or mocked for testing.
# Conclusion

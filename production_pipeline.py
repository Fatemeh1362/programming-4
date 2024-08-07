import os
import json
import logging
import pandas as pd
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pipeline_model import ModelPipeline
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

class BasePipeline(ABC):
    """
    abstract base class for pipeline processing with common functionality.

    Attributes:
        config_path (str): Path to the configuration file.
        input_dir (str): Directory where input files are located.
        output_dir (str): Directory where output files will be saved.
        img_dir (str): Directory where images will be saved.
        sensors_to_plot (List[str]): List of sensors for which anomalies will be plotted.
        check_interval (int): Interval in seconds for checking new files.
        model_path (str): Path to the model file.
    """
    def __init__(self, config_path: str):
        """
        initializes the pipeline with configuration settings.

        Args:
            config_path (str): Path to the configuration JSON file.
        """
        self.config_path = config_path

        # Again why do you need to initialize all these fields with a value of None?
        self.input_dir = None
        self.output_dir = None
        self.img_dir = None
        self.sensors_to_plot = []
        self.check_interval = 30
        self.model_path = None
        self.load_config()
        self.setup_logging()

    @abstractmethod
    def process_new_file(self, file_path: str):
        """
        Abstract method to process a new file. To be implemented by subclasses.

        Args:
            file_path (str): Path to the file to be processed.
        """
        pass

    def load_config(self):
        """
        Load configuration from JSON file.

        Reads settings from the configuration file and sets up necessary directories and parameters.
        """
        try:
            with open(self.config_path, 'r') as file:
                config = json.load(file)
                self.input_dir = config.get('input_directory', './input')
                self.output_dir = config.get('output_directory', './output')
                self.img_dir = config.get('img_directory', './img')
                self.sensors_to_plot = config.get('sensors_to_plot', [])
                self.check_interval = config.get('check_interval', 30)
                self.model_path = config.get('model_path', 'model.pkl')
            logging.info("Configuration loaded.")
        except FileNotFoundError:
            logging.error("Configuration file not found.")
            raise
        except json.JSONDecodeError:
            logging.error("Error decoding JSON configuration file.")
            raise

    def setup_logging(self):
        """
        Set up logging.

        Configures logging to output messages to a file named 'production_pipeline.log'.
        """
        logging.basicConfig(filename='production_pipeline.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging setup complete.")

# Again a way too complex class
class ProductionPipeline(BasePipeline):
    """
     implementation of a production pipeline.

    Inherits from BasePipeline and implements file processing and directory monitoring.
    """

    def __init__(self, config_path: str):
        """
        Initializes the production pipeline.

        Args:
            config_path (str): Path to the configuration JSON file.
        """
        super().__init__(config_path)
        self.executor = ThreadPoolExecutor(max_workers=4)  # Using parallelization for file processing

    def process_new_file(self, file_path: str):
        """
        Process a new file by generating predictions and plots.

        Args:
            file_path (str): Path to the new data file to process.
        """
        logging.info("Found new data file %s", file_path)
        try:
            model_pipeline = ModelPipeline(model_path=self.model_path, data_dir=self.input_dir)
            predictions = model_pipeline.process_new_data(file_path)
            output_path = os.path.join(self.output_dir, os.path.basename(file_path))
            pd.DataFrame(predictions, columns=['predictions']).to_csv(output_path, index=False)
            logging.info("Predictions saved to %s", output_path)
            
            # Using parallelization to plot sensors
            futures = [self.executor.submit(model_pipeline.plot_sensor_anomalies, sensor) for sensor in self.sensors_to_plot]
            for future in futures:
                plot_file = future.result()
                logging.info("Saving image %s", plot_file)
            
            os.remove(file_path)
            logging.info("Removed original data file %s", file_path)
        except Exception as e:
            logging.error("Error processing file %s: %s", file_path, str(e))

    def start_monitoring(self):
        """
        start monitoring the input directory for new files.

        Using watchdog to monitor the input directory and processes new files as they appear.
        """
        event_handler = FileSystemEventHandler()
        event_handler.on_created = lambda event: self.executor.submit(self.process_new_file, event.src_path)
        observer = Observer()
        observer.schedule(event_handler, self.input_dir, recursive=False)
        observer.start()
        logging.info("Started listening for new files.")
        try:
            while True:
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

import os
import json
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pipeline_model import ModelPipeline

class ProductionPipeline:
    def __init__(self, config_path):
        self.config_path = config_path
        self.input_dir = None
        self.output_dir = None
        self.img_dir = None
        self.sensors = None
        self.check_interval = None
        self.load_config()
        self.setup_logging()

    def load_config(self):
        with open(self.config_path, 'r') as file:
            config = json.load(file)
            self.input_dir = config['input_directory']
            self.output_dir = config['output_directory']
            self.img_dir = config['img_directory']
            self.sensors = config['sensors']
            self.check_interval = config['interval']
        logging.info("Configuration loaded.")

    def setup_logging(self):
        logging.basicConfig(filename='production_pipeline.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging setup complete.")

    def process_new_file(self, file_path):
        logging.info("Found new data file %s", file_path)
        try:
            model_pipeline = ModelPipeline(model_path='model.pkl', data_dir=self.input_dir)
            predictions = model_pipeline.process_new_data(file_path)
            output_path = os.path.join(self.output_dir, os.path.basename(file_path))
            pd.DataFrame(predictions, columns=['predictions']).to_csv(output_path, index=False)
            logging.info("Predictions saved to %s", output_path)

            # Generate plots for sensors
            for sensor in self.sensors:
                plot_file = model_pipeline.plot_sensor_anomalies(sensor)
                logging.info("Saving image %s", plot_file)

            # Remove the processed file
            os.remove(file_path)
            logging.info("Removed original data file %s", file_path)
        except Exception as e:
            logging.error("Error processing file %s: %s", file_path, str(e))

    def run(self):
        event_handler = FileSystemEventHandler()
        event_handler.on_created = lambda event: self.process_new_file(event.src_path)
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

import paho.mqtt.client as mqtt  # type: ignore
import numpy as np
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate(median=90, err=10, outlier_err=30, size=1000, outlier_size=10):
    logging.debug("Generating normal error values.")
    errs = err * np.random.rand(size) * np.random.choice((-1, 1), size)
    data = median + errs

    logging.debug("Generating lower outliers.")
    lower_errs = outlier_err * np.random.rand(outlier_size)
    lower_outliers = median - err - lower_errs

    logging.debug("Generating upper outliers.")
    upper_errs = outlier_err * np.random.rand(outlier_size)
    upper_outliers = median + err + upper_errs

    data = np.concatenate((data, lower_outliers, upper_outliers))
    np.random.shuffle(data)

    logging.debug(f"Generated data pool of size {len(data)}.")
    return data

if __name__ == '__main__':
    logging.info("Starting MQTT data publisher.")

    # Environment variables
    broker = os.getenv("MQTT_BROKER", "mosquitto")
    rate = float(os.getenv("MQTT_RATE", 1))
    suffix = os.getenv("MQTT_SUFFIX", os.getenv("HOSTNAME", "1"))
    topic = f"sensor{suffix}/data"
    drift_enabled = os.getenv("DATA_DRIFT", "false").lower() == "true"
    drift_rate = float(os.getenv("DRIFT_RATE", 0.01))  # Rate of drift increase

    logging.info(f"Broker: {broker}")
    logging.info(f"Rate: {rate} seconds")
    logging.info(f"Topic: {topic}")
    logging.info(f"Data drift enabled: {drift_enabled}")

    # Generate base data pool
    data = generate()

    client = mqtt.Client()
    client.connect(broker, 1883, 60)
    client.loop_start()

    drift_offset = 0

    try:
        while True:
            value = np.random.choice(data)
            if drift_enabled:
                drift_offset += drift_rate
                value += drift_offset

            message = str(round(value, 2))
            logging.debug(f"Publishing message: {message}")
            client.publish(topic, payload=message)
            time.sleep(rate)
    except KeyboardInterrupt:
        logging.info("MQTT publisher stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
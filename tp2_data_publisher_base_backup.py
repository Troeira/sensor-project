import numpy as np
import logging
import time
import paho.mqtt.client as mqtt

def generate(median=50, err=10, outlier_err=30, size=1000, outlier_size=10):
    logging.debug("Generating normal error values.")
    errs = err * np.random.rand(size) * np.random.choice((-1, 1), size)
    data = median + errs
    data = np.clip(data, 0, 100)

    logging.debug("Generating lower outliers.")
    lower_errs = outlier_err * np.random.rand(outlier_size)
    lower_outliers = median - err - lower_errs
    lower_outliers = np.clip(lower_outliers, 0, 100)

    logging.debug("Generating upper outliers.")
    upper_errs = outlier_err * np.random.rand(outlier_size)
    upper_outliers = median + err + upper_errs
    upper_outliers = np.clip(upper_outliers, 0, 100)

    data = np.concatenate((data, lower_outliers, upper_outliers))
    np.random.shuffle(data)

    logging.debug(f"Generated data pool of size {len(data)}.")
    return data

if __name__ == '__main__':
    logging.info("Starting MQTT data publisher.")
    
    broker = "mosquitto"
    rate = 1
    topic = "sensor/data"
    
    logging.info("Starting MQTT data publisher.")
    logging.info(f"Using broker: {broker}")
    logging.info(f"Publishing rate: {rate} seconds")
    logging.info(f"Topic: {topic}")

    data = generate()

    client = mqtt.Client()
    client.connect(broker, 1883, 60)
    client.loop_start()

    try:
        while True:
            message = str(np.random.choice(data))
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

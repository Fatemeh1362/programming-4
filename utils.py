import matplotlib.pyplot as plt

def plot_sensor_anomalies(sensor_id, title, data):
    # Example plotting function
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data[sensor_id], label='Sensor Data')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Sensor Value')
    plt.legend()
    return plt

def save_plot(plt, filename):
    plt.savefig(filename)
    plt.close()

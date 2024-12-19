import pandas as pd
import matplotlib.pyplot as plt
import time

log_file = "./logs/metric_log.csv"
output_file = "./logs/error_distribution.png"

while True:
    try:
        if os.path.exists(log_file):
            data = pd.read_csv(log_file)
            plt.figure(figsize=(10, 6))
            plt.hist(data["absolute_error"], bins=20, color='blue', alpha=0.7)
            plt.title("Распределение абсолютных ошибок")
            plt.xlabel("Absolute Error")
            plt.ylabel("Frequency")
            plt.grid()
            plt.savefig(output_file)
            print(f"Гистограмма обновлена: {output_file}")
        time.sleep(5)
    except Exception as e:
        print(f"Ошибка при построении графика: {e}")
    

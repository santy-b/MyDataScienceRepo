import requests
import os
import pandas as pd
import matplotlib.pyplot as plt

class Trasformer:
    def __init__(self):
        self.data_frame = None
    
    def download_csv_to_pandas(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.basename(url)
            with open(filename, "wb") as f:
                f.write(response.content)
            self.data_frame = pd.read_csv(filename, header=None)
            return self.data_frame
        else:
            raise Exception(f"Failed to download {url}")
    
    def csv_to_pandas(self, csv_file):
        data_frame = pd.read_csv(csv_file, header=None)
        self.data_frame = data_frame
        return self.data_frame
    
    def column_names(self, names_list):
        if len(names_list) != len(self.data_frame.columns):
            raise ValueError("Number of column names does not match the number of DataFrame columns")
        self.data_frame.columns = names_list

    def get_shape(self):
        rows, columns = self.data_frame.shape
        print("Rows:", rows, "Columns:", columns)

    def plot_df(self, x_column, y_column):
        plt.figure()
        plt.plot(self.data_frame[x_column], self.data_frame[y_column])
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title("Scatter Plot of DataFrame")
        plt.show()

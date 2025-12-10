import os
import pandas as pd
 
class CSVExtractor:
    def extract(self, file_path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        raw_data_dir = os.path.normpath(os.path.join(base_dir,'..','..','data','raw'))
        csv_path = os.path.join(raw_data_dir, file_path)
 
        try:
            if not os.path.exists(csv_path):
                return None
           
            if os.path.getsize(csv_path) == 0:
                return pd.DataFrame()
           
            data = pd.read_csv(csv_path)
            return data
        except Exception as e:
            print(f"Error reading {csv_path}: {e}")
            return None
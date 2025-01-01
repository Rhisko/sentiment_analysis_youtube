import csv
import logging
from typing import List, Dict
import os


def save_to_csv(file_path: str, data, fieldnames: List[str]= None):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write data to CSV
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            if fieldnames is not None:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            else:
                for commment in data:
                     file.write(commment + "\n") 
                
        logging.info(f"File saved successfully: {file_path}")
    except Exception as e:
        logging.error(f"Error saving file {file_path}: {e}")
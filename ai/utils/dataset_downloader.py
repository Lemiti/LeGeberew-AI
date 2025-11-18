# ai/utils/dataset_downloader.py
import os
import kaggle
import zipfile

def download_dataset():
    """Download PlantVillage dataset from Kaggle"""
    dataset_slug = "emmarex/plantdisease"
    download_path = "data/raw"
    
    # Create directory
    os.makedirs(download_path, exist_ok=True)
    
    try:
        # Download dataset (you'll need to set up Kaggle API first)
        kaggle.api.dataset_download_files(dataset_slug, path=download_path, unzip=True)
        print("Dataset downloaded successfully!")
        
        # Reorganize if needed
        reorganize_dataset()
        
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        print("Please download manually from: https://www.kaggle.com/datasets/emmarex/plantdisease")
        print("And extract to data/raw/")

def reorganize_dataset():
    """Reorganize dataset structure if needed"""
    # This depends on the dataset structure
    # You might need to move files around
    pass

# Run this to download
if __name__ == "__main__":
    download_dataset()
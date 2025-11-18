# ai/utils/verify_dataset.py
import os
import glob

def verify_dataset_structure():
    dataset_path = "data/raw/PlantVillage"
    
    if not os.path.exists(dataset_path):
        print("❌ Dataset path not found!")
        return False
    
    print("🔍 Checking dataset structure...")
    
    # List all directories (should be plant disease folders)
    all_items = os.listdir(dataset_path)
    directories = [d for d in all_items if os.path.isdir(os.path.join(dataset_path, d))]
    
    print(f"📁 Found {len(directories)} plant disease categories:")
    
    for dir_name in directories[:10]:  # Show first 10
        dir_path = os.path.join(dataset_path, dir_name)
        images = glob.glob(os.path.join(dir_path, "*.JPG")) + glob.glob(os.path.join(dir_path, "*.jpg"))
        print(f"   🌱 {dir_name}: {len(images)} images")
    
    if len(directories) > 10:
        print(f"   ... and {len(directories) - 10} more categories")
    
    # Check total images
    all_images = glob.glob(os.path.join(dataset_path, "**/*.JPG")) + glob.glob(os.path.join(dataset_path, "**/*.jpg"))
    print(f"📊 Total images: {len(all_images)}")
    
    return len(all_images) > 0

if __name__ == "__main__":
    verify_dataset_structure()
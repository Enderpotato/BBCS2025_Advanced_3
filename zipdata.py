import zipfile
import os
# take the dataset folder and zip it into a .zip file for easier commit

DATASET_PATH = 'dataset'
ZIP_FILE_NAME = 'data.zip'

def zip_dataset():
    with zipfile.ZipFile(ZIP_FILE_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(DATASET_PATH):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, DATASET_PATH))
    print(f'Dataset zipped into {ZIP_FILE_NAME}')

if __name__ == "__main__":
    zip_dataset()
    print("Done zipping the dataset.")
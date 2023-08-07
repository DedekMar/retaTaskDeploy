import requests
import zipfile
import os
import shutil
import argparse

# Download the zip file, save it to a temporary file, extract contents to target folder, delete temporary file
def download_and_extract_zip(url, target_directory):
    try:
        
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        # Download the zip file from the URL first using stream
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            print(f"Failed to download the ZIP file from {url}")
            return False

        temp_zip_file = os.path.join(target_directory, "temp_export.zip")

        with open(temp_zip_file, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

        response.close()

        # Extract the contents of the ZIP file
        with zipfile.ZipFile(temp_zip_file, "r") as zip_ref:
            zip_ref.extractall(target_directory)

        # Delete the temporary ZIP file
        os.remove(temp_zip_file)    

        print("The zip file has been sucessfuly downloaded and extracted")
        return True

    except Exception as e:
        print(f"Error downloading or extracting the zip file: {e}")
        return False
    

# Default arguments set to the url provided in task and the project main directory
if __name__ == "__main__":

    default_url = "https://www.retailys.cz/wp-content/uploads/astra_export_xml.zip"
    default_target_directory = "."  

    parser = argparse.ArgumentParser(description="Save and extract the zip file from specified url")
    
    # Add command-line arguments for url and target directory
    parser.add_argument("-url", default = default_url, help="URL location of the zip file")
    parser.add_argument("-td", default = default_target_directory, help="Path to target directory, where file will be extracted to")

    args = parser.parse_args()
    url = args.url
    target_directory = args.td

    success = download_and_extract_zip(url, target_directory)
    if success :
        print("XML file downloaded and extracted successfully")

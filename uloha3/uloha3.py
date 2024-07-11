import csv
import requests
import configparser

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Save values from config to variables
API_URL = config['invoicer']['api_url']
CSV_FILE_PATH = config['invoicer']['csv_file_path']
ZONE_ID = config['invoicer']['zone_id']

# Function which will set ZoneID, takes invoice_filename as a parameter
# It will return either 0(ok) or 1(error)
def set_zone_id(invoice_filename):
     # Construct URL for the request
    url = f"{API_URL}?invoice={invoice_filename}&value={ZONE_ID}"

    # Try to make a GET request to URL, if it is succesful return 0
    try: 
        response = requests.get(url)
        print(f"Request for {invoice_filename}: {response.status_code}")
        return 0
    # If there is an exception during request call, throw an exception
    except request.exceptions.RequestException as e:
        print(f"Request failed for {invoice_filename}:{e}")
        return 1

# Main method
def main():
    try:
        # Try to open CSV file with specified path
        with open(CSV_FILE_PATH,'r') as csvfile:
            # Read the csv file as a dictionary, so we can access the data using the column names
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Create variable with invoice filename as requested
                invoice_filename = f"{row['invoice_prefix']}-{row['fromdate']}-{row['todate']}.pdf"
                # Call the function the set the ZoneID
                set_zone_id(invoice_filename)

    # If the csv file does not exists, throw an exception
    except FileNotFoundError:
        print(f"Error: File {CSV_FILE_PATH} not found.")
    # If anything else fails, throw an exception
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
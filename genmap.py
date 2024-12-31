from geopy.geocoders import Nominatim
from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass
import csv

DATA_FILE_PATH = "data.csv"
DATA_NAME_COLUMN = "Name"
DATA_ZIPCODE_COLUMN = "Primary Zip"

@dataclass
class Pin:
    zip_code: str
    latlong: str
    count: int


def create_html_file(pins):
    """Create HTML file from template using provided pins data."""
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html.j2')
    output = template.render(pins=pins)

    with open('index.html', 'w') as file:
        file.write(output)


def zip_to_latlong(zip_code):
    """Convert ZIP code to latitude/longitude coordinates."""
    geolocator = Nominatim(user_agent="zip_to_latlong_app")
    location = geolocator.geocode(zip_code)
    if location:
        return f"{location.latitude},{location.longitude}"
    return None


def main():
    """Main function to process CSV data and generate HTML map."""
    pin_lookup = {}  # Changed from camelCase to snake_case

    with open(DATA_FILE_PATH, mode='r') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:
            print("Debug:", row)
            zip_code = row[DATA_ZIPCODE_COLUMN]
            
            if zip_code in pin_lookup:
                pin_lookup[zip_code].count += 1
            else:
                pin_lookup[zip_code] = Pin(zip_code, None, 1)

    for pin in pin_lookup.values():
        print(f"Zip: {pin.zip_code} - Count: {pin.count}")
        latlong = zip_to_latlong(pin.zip_code)
        if latlong:
            pin.latlong = latlong

    create_html_file(pin_lookup.values())


if __name__ == "__main__":
    main()
import csv
import json
import os

def csv_to_geojson(input_csv, output_geojson):
    """
    Reads a CSV file with spatial data and converts it into a GeoJSON format.
    """

    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    try:
        # Open the raw CSV file
        with open(input_csv, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            # Iterate through each row in the CSV
            for row in csv_reader:
                # Extract coordinates and convert them to floats
                lat = float(row['Latitude'])
                lon = float(row['Longitude'])
                
                # Create a single GeoJSON feature
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat] # GeoJSON standard is [Longitude, Latitude]
                    },
                    "properties": {
                        "Facility_ID": row['Facility_ID'],
                        "Facility_Type": row['Facility_Type'],
                        "Location_Name": row['Location_Name'],
                        "Operator": row['Operator'],
                        "Status": row['Status']
                    }
                }
                
                # Add the feature to our collection
                geojson_data['features'].append(feature)
                
        # Write the structured data to a new GeoJSON file
        with open(output_geojson, mode='w', encoding='utf-8') as geojson_file:
            json.dump(geojson_data, geojson_file, indent=4)
            
        print(f"Success! Converted {input_csv} to {output_geojson}")

    except Exception as e:
        print(f"Error processing the file: {e}")

# --- Execution block ---
if __name__ == "__main__":
    # Define file names
    INPUT_FILE = 'texas_energy_infrastructure.csv'
    OUTPUT_FILE = 'texas_energy_infrastructure.geojson'
    
    # Check if input file exists before running
    if os.path.exists(INPUT_FILE):
        csv_to_geojson(INPUT_FILE, OUTPUT_FILE)
    else:
        print(f"File {INPUT_FILE} not found. Please ensure it is in the same directory.")
# spatial-data-automator
Python script to convert raw CSV infrastructure data into GeoJSON format
## Project Overview
This project is a lightweight, automated data  pipeline built in Python. It is designed to ingest raw tabular spatial data (such as infrastructure locations or environmental monitoring stations) and automatically convert it into the web-standard GeoJSON format. 

## Tech Stack
* **Language:** Python 3.13
* **Libraries:** `csv`, `json`, `os` (Standard libraries used to ensure fast execution and easy migration to serverless cloud environments like AWS Lambda).
* **Data Standard:** GeoJSON

## How It Works
1. **Input:** Reads a raw `.csv` file containing latitude, longitude, and attribute data.
2. **Processing:** The Python script parses the coordinates and isolates the spatial geometry from the descriptive properties.
3. **Structuring:** It restructures the data into a standard `FeatureCollection` schema.
4. **Export:** Generates a clean `.geojson` file ready for deployment.

## Use Case Example
The current dataset (`texas_energy_infrastructure.csv`) uses sample environmental air quality monitoring data from the Gulf Coast region. The script successfully transforms this tabular data into a spatial format that can be easily visualized in digital twins or cloud-based maps.

## Next Steps (Cloud Integration)
* [ ] Containerize the application using Docker.
* [ ] Migrate the Python script to **AWS Lambda** for serverless, event-driven execution triggered by Amazon S3 uploads.

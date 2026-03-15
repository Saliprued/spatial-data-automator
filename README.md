# spatial-data-automator
Python script to convert raw CSV infrastructure data into GeoJSON format. This architecture provides a scalable, low-latency solution to integrate sensitive or rapidly changing spatial information into centralized dashboards.

## Overview
This project is a lightweight, automated data  pipeline built in Python. It is designed to ingest raw tabular spatial data (such as infrastructure locations or environmental monitoring stations) and automatically convert it into the web-standard GeoJSON format. 

By integrating Cloud Computing (AWS) with Geospatial Information Systems (GIS), this pipeline eliminates the need for manual map updates. When new infrastructure data (CSV) is ingested, the system automatically processes it into web-ready spatial formats (GeoJSON) and updates a live interactive web map in real-time.

## Cloud & Web Architecture
The system is built using a serverless, event-driven architecture to ensure scalability and low maintenance:

1. **Data Input:** __AWS S3__ acts as the primary data lake. Raw infrastructure data (`.csv`) is uploaded to a secure bucket.
2. **Serverless Processing:** __Lamdda & Python__ Python script utilizing standard libraires like `csv`, `json`, `os` and `boto3` which is triggered automatically upon new file uploads. It reads the raw data, processes and generates a structured `.geojson` file.
3. **Live Data Hosting:**  __AWS S3 & CORS__ the processed GeoJSON is stored back in S3 with Cross-Origin Resource Sharing (CORS) configured, securely serving the spatial data to the frontend via Object URLs.
4. **Interactive Web Interface:** __TML/CSS/JS & Leaflet.js__ a lightweight, responsive web map hosted on **GitHub**. Using the JavaScript `fetch()` API, it dynamically retrieves the latest `.geojson` directly from the AWS S3 bucket, ensuring users always see the most up-to-date infrastructure network without requiring manual code deployments.

## Use Case Example
The current dataset (`texas_energy_infrastructure.csv`) uses sample environmental air quality monitoring data from the Gulf Coast region. The script successfully transforms this tabular data into a spatial format that can be easily visualized in digital twins or cloud-based maps.

## About the Developer
I am a geospatial data professional holding a Master's degree in GIS, with a strong background in geosciences, geomatics, and spatial data management. Currently expanding my technical stack through a Web Application Development and Cloud Computing program, my goal is to bridge the gap between complex spatial analysis and modern cloud architectures to build automated.







# Power BI and Pentaho Analysis Project

## Overview

This project involves the integration of several components to process and visualize data using Power BI, Pentaho PDI, PostgreSQL, and a Python-based backend server. The project is designed to update, transform, and load data efficiently, which is then visualized using Power BI dashboards.

## Project Components

1. **Backend Server**: 
   - Handles data updates and serves as the initial point of contact for the Pentaho jobs.

2. **Pentaho PDI (Pentaho Data Integration)**:
   - Initiates the data update process by calling the backend server.
   - Performs data transformations.
   - Creates dimension and fact tables in the PostgreSQL database.

3. **PostgreSQL**:
   - Stores the transformed data in structured tables.
   - Acts as the data source for Power BI.

4. **Power BI**:
   - Fetches data from the PostgreSQL database.
   - Visualizes the data in interactive dashboards.

## Data Processing Workflow

1. **Data Update**: 
   - Pentaho jobs call the backend server to update the data.

2. **Data Transformation**:
   - After updating, data transformations are performed.

3. **Table Creation**:
   - Dimension and fact tables are created in the PostgreSQL database.

4. **Data Loading**:
   - Transformed data is loaded into the specific tables.

5. **Data Visualization**:
   - Power BI fetches the data from the database and displays it in the dashboard.

## Machine Learning Model

The project includes a classification model that analyzes prisoners' data. The model is trained to classify the facility of the prisoners and detect whether they were held by the Israeli Police Service (IPS) or the Israeli Defence Force (IDF).

## Conclusion

This project demonstrates a comprehensive data processing and visualization pipeline, integrating multiple technologies to deliver insights through Power BI dashboards.

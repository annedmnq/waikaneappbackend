# Waikāne Flooding Backend API

This is the backend API server for the Waikāne flooding monitoring system, providing real-time stream and tide data for flood prediction and monitoring.

## Features

- Real-time stream height data from USGS monitoring stations
- Serves rainfall data in the last hour
- Tide level predictions and current conditions
- Flood threshold analysis and alerts
- Data visualization generation
- RESTful API endpoints for frontend consumption

## API Endpoints

### Stream Data
- `http://149.165.159.226:5000/api/waikane_stream` - Get data on Waikāne stream height
- `http://149.165.159.226:5000/api/waiahole_stream` - Get data on Waiāhole stream height
- `http://149.165.159.226:5000/api/punaluu_stream` - Get data on Punalu'u stream height
- `http://149.165.159.226:5000/api/waikane_stream` - Get data on stream trends

### Tide Data
- `http://149.165.159.226:5000/api/waikane_tide_curve` - Gets data on Waikāne’s previous and predicted tide heights
- `http://149.165.159.226:5000/api/waikane_tides` - Gets data on Waikāne’s previous and predicted high tides and low tides


### Rain Data
- `http://149.165.159.226:5000/api/rain_data` - Gets data on the amount of rainfall in the last hour and last 6 hours in the Makai and Mauka areas

## Data Sources

- **USGS Water Services**: Real-time stream gauge data
- **NOAA Tides & Currents**: Tide predictions and observations

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <https://github.com/annedmnq/waikaneappbackend.git>
   cd waikaneappbackend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API server**
   ```bash
   python api.py
   ```

4. **Access the API**
   - Server runs on Jetstream
   - API documentation available at endpoints above

## Data Files

### Stream Data
- `Waikane_Stream_Data.json` - Waikāne stream data
- `Waiahole_Stream_Data.json` - Waiāhole stream data
- `Punaluu_Stream_Data.json` - Punalu'u stream data
- `Stream_Trend_Data.json` - Stream trend data

### Tide Data
- `Waikane_Tide_Data.json` - High and low tide observations for Waikāne
- `Waikane_Tide_Curve.json` - Past and predicted tide levels for Waikāne
- `1612480_tide_predictions.csv` - NOAA tide predictions for Mokuoloe

### Flood Thresholds
- `Flooding_Thresholds/Waikane_16294900_stream_flood_thresholds.csv`
- `Flooding_Thresholds/Waiahole_16294100_stream_flood_thresholds.csv`
- `Flooding_Thresholds/Mokuoloe-Waikane_tide_flood_thresholds.csv`
- `Flooding_Thresholds/Poamoho_rain_gauge_thresholds.csv`
- `Flooding_Thresholds/Waiahole_rain_gauge_thresholds.csv`

## Data Analysis

- `Waikane_Flood_Visuals.ipynb` - Jupyter notebook for data analysis
- `run_notebook.py` - Script to execute notebook programmatically

## Configuration

The API server is configured to:
- Accept CORS requests from frontend applications
- Serve data in JSON format
- Handle real-time data fetching from external sources
- Process and filter data based on current conditions

## Development

To add new endpoints or modify data processing:

1. Edit `api.py` for new routes
2. Update data processing logic in the respective functions
3. Add new threshold files to `Flooding_Thresholds/` as needed
4. Test endpoints using tools like Postman or curl

## Deployment

For production deployment:

1. Set up environment variables for API keys if needed
2. Configure proper CORS settings for your domain
3. Set up process management (PM2, systemd, etc.)
4. Configure reverse proxy (nginx) if needed
5. Set up SSL certificates for HTTPS

## License

This project is developed for flood monitoring and public safety in the Waikāne area.
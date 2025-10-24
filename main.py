import pandas as pd

print("Pandas version:", pd.__version__)

file_path = "vamosszabadi_atlag10m.xlsx"


# # Get all available sheet names
# sheet_names = pd.ExcelFile(file_path).sheet_names
# print(sheet_names)

# Read Excel file: skip first 5 rows, read 4 columns as strings
df1 = pd.read_excel(
    file_path,
    sheet_name="GPS Data",
    skiprows=4,
    usecols="A:D",
    names=["Station_km", "Latitude", "Longitude", "Altitude"],
    dtype=str,
)
# Drop any completely empty rows
df1 = df1.dropna(how="all")

# print(df.head())


# Define a simple data class for coordinates
class GpsPoint:
    def __init__(self, station_km, latitude, longitude, altitude):
        self.station_km = float(station_km)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.altitude = float(altitude)

    def __repr__(self):
        return f"GpsPoint(km={self.station_km}, lat={self.latitude}, lon={self.longitude}, alt={self.altitude})"


# Convert DataFrame rows into a list of objects
points = [
    GpsPoint(row["Station_km"], row["Latitude"], row["Longitude"], row["Altitude"])
    for _, row in df1.iterrows()
]

# # Print first few objects
# for p in points[:5]:
#     print(p)

# print(points.__len__())
print(points[-1])

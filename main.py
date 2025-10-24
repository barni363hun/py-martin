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
# print(points[-1])

# Read Excel file: skip first 5 rows, read 4 columns as strings
df2 = pd.read_excel(
    file_path,
    sheet_name="GPS Data",
    skiprows=4,
    usecols="F:I",
    names=["Station_km", "Latitude", "Longitude", "Altitude"],
    dtype=str,
)

df1_last_value = points[-1]

# Drop any completely empty rows
df2 = df2.dropna(how="all")

points_2 = [
    GpsPoint(row["Station_km"], row["Latitude"], row["Longitude"], row["Altitude"])
    for _, row in df2.iterrows()
]

for p in points_2:
    p.station_km += df1_last_value.station_km
    points.append(p)

# print(points.__len__())
# print(points[14930])  # last from df1
# print(points[14931])  # first from df2


# Read Excel file: skip first 5 rows, read 4 columns as strings
df3 = pd.read_excel(
    file_path,
    sheet_name="GPS Data",
    skiprows=4,
    usecols="K:N",
    names=["Station_km", "Latitude", "Longitude", "Altitude"],
    dtype=str,
)

df2_last_value = points[-1]

# Drop any completely empty rows
df3 = df3.dropna(how="all")

points_3 = [
    GpsPoint(row["Station_km"], row["Latitude"], row["Longitude"], row["Altitude"])
    for _, row in df3.iterrows()
]

for p in points_3:
    p.station_km += df2_last_value.station_km
    points.append(p)

print(points.__len__())
# print(points[14930])  # last from df1
# print(points[14931])  # first from df2
# print(points[20811])  # last from df2
# print(points[20812])  # first from df2

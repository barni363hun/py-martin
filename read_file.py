import pandas as pd


print("Pandas version:", pd.__version__)

file_path = "vamosszabadi_atlag10m.xlsx"


# # Get all available sheet names
# sheet_names = pd.ExcelFile(file_path).sheet_names
# print(sheet_names)
# ['Rutting (RSP)', 'Mean Profile Depth', 'GPS Data', 'IRI (RSP)']

"""
GPS Data			
Kilometres			
Station	Latitude	Longitude	Altitude
km			
0.000	47.748456	17.649050	105.850000
0.000	47.748438	17.649067	108.390000
0.000	47.748438	17.649067	108.440000
0.000	47.748430	17.649074	111.330000
0.000	47.748431	17.649075	111.350000
0.001	47.748431	17.649076	111.330000
0.001	47.748432	17.649077	111.370000
0.001	47.748433	17.649078	111.380000
0.001	47.748434	17.649079	111.380000
0.001	47.748435	17.649080	111.370000
0.001	47.748436	17.649081	111.440000
0.002	47.748437	17.649083	111.440000
"""

class GpsData:
    def __init__(self, station_km, lat, lon, alt):
        self.station_km = float(station_km)
        self.latitude = float(lat)
        self.longitude = float(lon)
        self.altitude = float(alt)

    def __repr__(self):
        return f"GpsPoint(km={self.station_km}, lat={self.latitude}, lon={self.longitude}, alt={self.altitude})"

"""
Rutting (RSP)								
Kilometres								
From	To	Left	Center	Right	Left Max	Center Max	Right Max	Average Left\Right
km	km	mm	mm	mm	mm	mm	mm	mm
0.000	0.010	2.62	5.36	3.49	5.11	9.24	7.21	3.06
0.010	0.020	0.46	1.51	1.09	1.11	2.50	1.96	0.78
0.020	0.030	0.57	1.23	1.12	1.19	1.90	1.77	0.85
0.030	0.040	0.25	1.29	1.00	0.81	1.83	1.55	0.63
0.040	0.050	0.30	1.09	0.71	0.74	1.73	1.44	0.51
0.050	0.060	0.63	1.05	0.68	1.29	1.78	1.33	0.66
0.060	0.070	0.48	0.83	0.72	1.03	1.43	1.35	0.60
0.070	0.080	0.50	0.69	0.59	0.95	1.04	0.97	0.55
"""

class RuttingData:
    def __init__(self, from_km, to_km, left, center, right, left_max, center_max, right_max, avg_lr):
        self.from_km = float(from_km)
        self.to_km = float(to_km)
        self.left = float(left)
        self.center = float(center)
        self.right = float(right)
        self.left_max = float(left_max)
        self.center_max = float(center_max)
        self.right_max = float(right_max)
        self.avg_lr = float(avg_lr)

    def __repr__(self):
        return f"RuttingData(from={self.from_km}, to={self.to_km}, left={self.left}, center={self.center}, right={self.right}, left_max={self.left_max}, center_max={self.center_max}, right_max={self.right_max}, avg_lr={self.avg_lr})"

"""
Mean Profile Depth				
Kilometres				
From	To	Left	Right	Average Left\Right
km	km	mm	mm	µm
0.000	0.010	0.857	1.059	957.850
0.010	0.020	0.824	0.953	888.200
0.020	0.030	0.809	0.957	883.200
0.030	0.040	0.846	0.989	917.550
0.040	0.050	0.911	1.037	973.700
0.050	0.060	1.072	1.050	1,061.150
0.060	0.070	0.955	1.248	1,101.250
0.070	0.080	0.749	1.157	953.100
"""

class MPDData:
    def __init__(self, from_km, to_km, left, right, avg_lr):
        self.from_km = float(from_km)
        self.to_km = float(to_km)
        self.left = float(left)
        self.right = float(right)
        self.avg_lr = float(avg_lr.replace(",", ""))  # remove thousands separator

    def __repr__(self):
        return f"MPDData(from={self.from_km}, to={self.to_km}, left={self.left}, right={self.right}, avg_lr={self.avg_lr})"

"""
IRI (RSP)					
Kilometres					
From	To	Left	Center	Right	Average Left\Right
km	km	m/km	m/km	m/km	m/km
0.000	0.010	1.59	1.76	2.71	2.15
0.010	0.020	4.31	3.27	3.65	3.98
0.020	0.030	3.53	2.41	2.60	3.07
0.030	0.040	2.25	2.07	1.80	2.03
0.040	0.050	2.74	2.51	2.59	2.67
0.050	0.060	6.04	6.54	3.92	4.98
0.060	0.070	6.06	5.16	4.22	5.14
0.070	0.080	2.95	3.02	3.65	3.30
"""

class IRIData:
    def __init__(self, from_km, to_km, left, center, right, avg_lr):
        self.from_km = float(from_km)
        self.to_km = float(to_km)
        self.left = float(left)
        self.center = float(center)
        self.right = float(right)
        self.avg_lr = float(avg_lr)

    def __repr__(self):
        return f"IRIData(from={self.from_km}, to={self.to_km}, left={self.left}, center={self.center}, right={self.right}, avg_lr={self.avg_lr})"

def read_points(sheet, cols, offset=0):
    """Reads a block of GPS data and applies km offset."""
    df = pd.read_excel(
        file_path,
        sheet_name=sheet,
        skiprows=4,
        usecols=cols,
        names=["Station_km", "Latitude", "Longitude", "Altitude"],
        dtype=str,
    ).dropna(how="all")
    pts = [GpsData(*row) for row in df.to_numpy()]
    for p in pts:
        p.station_km += offset
    return pts


# Process each block sequentially
points = []
offset = 0
for cols in ["A:D", "F:I", "K:N"]:
    new_points = read_points("GPS Data", cols, offset)
    points.extend(new_points)
    offset = points[-1].station_km  # update for next block

print(len(points))
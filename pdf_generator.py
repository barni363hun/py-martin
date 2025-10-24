import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

print("Pandas version:", pd.__version__)

file_path = "vamosszabadi_atlag10m.xlsx"


class GpsPoint:
    def __init__(self, station_km, lat, lon, alt):
        self.station_km = float(station_km)
        self.latitude = float(lat)
        self.longitude = float(lon)
        self.altitude = float(alt)

    def __repr__(self):
        return f"GpsPoint(km={self.station_km}, lat={self.latitude}, lon={self.longitude}, alt={self.altitude})"


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
    pts = [GpsPoint(*row) for row in df.to_numpy()]
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

# Convert list of GpsPoint objects to a DataFrame for easier charting
data = {
    "Station_km": [p.station_km for p in points],
    "Latitude": [p.latitude for p in points],
    "Longitude": [p.longitude for p in points],
    "Altitude": [p.altitude for p in points],
}

df_all = pd.DataFrame(data)

# === Create charts ===
charts = []

# 1. Altitude vs Station
plt.figure(figsize=(8, 4))
plt.plot(df_all["Station_km"], df_all["Altitude"])
plt.xlabel("Station (km)")
plt.ylabel("Altitude (m)")
plt.title("Altitude Profile along the Route")
plt.grid(True)
buf1 = BytesIO()
plt.tight_layout()
plt.savefig(buf1, format="png")
plt.close()
buf1.seek(0)
charts.append(buf1)

# 2. Latitude vs Longitude
plt.figure(figsize=(6, 6))
plt.plot(df_all["Longitude"], df_all["Latitude"], linestyle="-", marker="", linewidth=1)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("GPS Track (Lat vs Lon)")
plt.grid(True)
buf2 = BytesIO()
plt.tight_layout()
plt.savefig(buf2, format="png")
plt.close()
buf2.seek(0)
charts.append(buf2)

# 3. Altitude Histogram
plt.figure(figsize=(6, 4))
plt.hist(df_all["Altitude"], bins=40)
plt.xlabel("Altitude (m)")
plt.ylabel("Frequency")
plt.title("Altitude Distribution")
plt.grid(True)
buf3 = BytesIO()
plt.tight_layout()
plt.savefig(buf3, format="png")
plt.close()
buf3.seek(0)
charts.append(buf3)

# === Create PDF report ===
pdf_filename = "gps_report.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("<b>GPS Data Report</b>", styles["Title"]))
story.append(Spacer(1, 0.3 * inch))
story.append(Paragraph(f"Total number of points: {len(points)}", styles["Normal"]))
story.append(Spacer(1, 0.2 * inch))

# Add charts to PDF
for i, chart in enumerate(charts, start=1):
    story.append(Paragraph(f"Chart {i}", styles["Heading2"]))
    story.append(Image(chart, width=6 * inch, height=3.5 * inch))
    story.append(Spacer(1, 0.3 * inch))

# Save the PDF
doc.build(story)

print(f"✅ PDF report saved as: {pdf_filename}")

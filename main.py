import pandas as pd

print("Pandas version:", pd.__version__)

# Path to your Excel file
file_path = "vamosszabadi_atlag10m.xlsx"

# Read the Excel file into a DataFrame
df = pd.read_excel(file_path)

# Display the first few rows
print(df.head())

# ecef_to_eci.py
#
# Usage: python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km
# Converts ECEF (Earth-Centered Earth-Fixed) coordinates to ECI (Earth-Centered Inertial) coordinates
# Parameters:
#  year: The year as an integer
#  month: The month as an integer (1-12)
#  day: The day as an integer (1-31)
#  hour: The hour as an integer (0-23)
#  minute: The minute as an integer (0-59)
#  second: The second as a float (can include a decimal portion)
#  ecef_x_km: The ECEF X-coordinate in kilometers
#  ecef_y_km: The ECEF Y-coordinate in kilometers
#  ecef_z_km: The ECEF Z-coordinate in kilometers
# Output:
#  Prints the ECI x, y, and z coordinates in km
#
# Written by Nick Davis
# Other contributors: None
#
# This work is licensed under CC BY-SA 4.0

# Import necessary modules
import math
import sys

# Constants
OMEGA_EARTH = 7.2921150e-5  # Earth's rotation rate in radians per second

# Helper function to calculate fractional Julian date
def ymdhms_to_jd(year, month, day, hour, minute, second):
    if month <= 2:
        year -= 1
        month += 12
    jd = math.floor(365.25*(year+4716))+math.floor(30.6001*(month+1))+day+(2-(math.floor(year/100))+ math.floor((math.floor(year/100))/4))-1524.5
    frac_day = (hour+minute/60.0+second/3600.0)/24.0
    return jd+frac_day

# Helper function to calculate the Greenwich Sidereal Time (GST) in radians
def gst_from_jd(jd):  
    T = (jd-2451545.0)/36525
    GMST_seconds = 67310.54841+(876600*60*60+8640184.812866)*T+0.093104*T**2-6.2e-6*T**3
    gst_rad = math.fmod(GMST_seconds%86400*OMEGA_EARTH+2*math.pi, 2*math.pi)
    return gst_rad

# Function to convert ECEF to ECI
def ecef_to_eci(jd, ecef_x_km, ecef_y_km, ecef_z_km):
    gst_rad = gst_from_jd(jd)
    
    # Inverse rotation matrix for ECEF to ECI
    eci_x_km = ecef_x_km*math.cos(-gst_rad)+ecef_y_km*math.sin(-gst_rad)
    eci_y_km = ecef_y_km*math.cos(-gst_rad)-ecef_x_km*math.sin(-gst_rad)
    eci_z_km = ecef_z_km
    
    return eci_x_km, eci_y_km, eci_z_km

# Parse script arguments
if len(sys.argv) == 10:
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])
    hour = int(sys.argv[4])
    minute = int(sys.argv[5])
    second = float(sys.argv[6])
    ecef_x_km = float(sys.argv[7])
    ecef_y_km = float(sys.argv[8])
    ecef_z_km = float(sys.argv[9])
else:
    print('Usage: python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km')
    exit()

# Calculate the Julian Date
jd = ymdhms_to_jd(year, month, day, hour, minute, second)

# Convert ECEF to ECI
eci_x_km, eci_y_km, eci_z_km = ecef_to_eci(jd, ecef_x_km, ecef_y_km, ecef_z_km)

# Print ECI coordinates in km
print(eci_x_km)
print(eci_y_km)
print(eci_z_km)
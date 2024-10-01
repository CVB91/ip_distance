import requests
import subprocess
import re
from math import radians, sin, cos, sqrt, atan2
import argparse


# Function to calculate distance between two lat/long points using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


# Get public IP info and location using ipinfo.io API
def get_ip_info(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    data = response.json()
    return data


# Get user's own location based on their public IP
def get_own_location():
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    if "loc" in data:
        lat, lon = map(float, data["loc"].split(","))
        return lat, lon
    else:
        raise Exception("Could not determine your location.")


# Ping the IP and get the round-trip time (RTT)
def get_ping_time(ip_address):
    try:
        ping_output = subprocess.run(
            ["ping", "-c", "4", ip_address], capture_output=True, text=True
        )
        # Extract average RTT from ping result
        avg_rtt = re.search(r"avg = ([0-9.]+)", ping_output.stdout)
        if avg_rtt:
            return float(avg_rtt.group(1))  # RTT in milliseconds
        else:
            return None
    except Exception as e:
        print(f"Error pinging {ip_address}: {e}")
        return None


# Main function
def estimate_distance(ip_address, custom_ip=None):
    # Get the location of the user's IP or the custom source IP if provided
    if custom_ip:
        print(f"Using custom IP: {custom_ip}")
        local_lat, local_lon = map(float, get_ip_info(custom_ip)["loc"].split(","))
    else:
        local_lat, local_lon = get_own_location()

    print(f"Source IP Location: Lat={local_lat}, Lon={local_lon}")

    # Get target IP location
    ip_info = get_ip_info(ip_address)
    if "loc" in ip_info:
        ip_lat, ip_lon = map(float, ip_info["loc"].split(","))
        print(f"Target IP Location: Lat={ip_lat}, Lon={ip_lon}")
        distance = haversine(local_lat, local_lon, ip_lat, ip_lon)
        print(f"Estimated Distance: {distance:.2f} km")

        # Get the round-trip time (RTT) and estimate distance based on RTT
        rtt = get_ping_time(ip_address)
        if rtt:
            speed_of_light_km_per_ms = (
                200  # Speed of light in fiber optics, approx. 200 km/ms
            )
            estimated_rtt_distance = (rtt / 2) * speed_of_light_km_per_ms
            print(
                f"RTT: {rtt} ms (Estimated Distance from RTT: {estimated_rtt_distance:.2f} km)"
            )
        else:
            print("Could not measure RTT.")
    else:
        print("Could not retrieve location for the IP address.")


# Command-line interface
def main():
    parser = argparse.ArgumentParser(
        description="Estimate distance between two IP addresses or from your own to a target IP."
    )
    parser.add_argument(
        "ip_address", type=str, help="The target IP address to analyze."
    )
    parser.add_argument(
        "--custom",
        type=str,
        help="Optional custom source IP address to calculate distance between two IPs.",
    )
    args = parser.parse_args()

    estimate_distance(args.ip_address, args.custom)


if __name__ == "__main__":
    main()

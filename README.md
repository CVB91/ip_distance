# IP Distance Tool

The **IP Distance Tool** is a Python command-line utility that calculates the estimated distance between two IP addresses using geolocation and Round-Trip Time (RTT) latency. It can either calculate the distance from your current location to a target IP or, using the `--custom` flag, between two specified IP addresses.

## Features

- Calculate distance between your public IP and a target IP address.
- Use geolocation data to determine the latitude and longitude of the IP addresses.
- Optionally, provide two custom IP addresses to calculate the distance between them.
- Measure RTT latency using the `ping` command and estimate distance based on network latency.
- Cross-platform support: Works on Linux, macOS, and Windows.

## Requirements

- Python 3.x
- `requests` library

Install the required dependencies using:

```bash
pip install -r requirements.txt

## How It Works

### Geolocation
The script uses the `ipinfo.io` API to fetch the latitude and longitude of both your public IP address (or custom IPs if provided) and the target IP address.

### Distance Calculation
The **Haversine formula** is used to calculate the great-circle distance between two sets of geographic coordinates, giving the distance in kilometers.

### RTT Measurement
The script uses the `ping` command to measure the Round-Trip Time (RTT) to the target IP address. It estimates the network distance by assuming data travels at approximately 200 km/ms in fiber optics.

## Features at a Glance

- **Haversine Formula**: Calculates the physical distance based on latitude and longitude.
- **RTT Calculation**: Measures network latency and estimates the distance based on data transmission speed.

## Known Issues

- **Permissions**: On Linux and macOS, the `ping` command may require elevated privileges. If you encounter permission issues, try running the script with `sudo`:
  
  ```bash
  sudo python ip_distance.py <target_ip>

- **Firewall Restrictions**: Some networks or ISPs block ping (ICMP) packets. If the script cannot measure RTT, check your network settings or try another network.

- **OS-Specific Differences**: The output format of ping differs across operating systems (Linux/macOS vs. Windows). The script handles both formats, but make sure you’re using the correct ping command for your OS.
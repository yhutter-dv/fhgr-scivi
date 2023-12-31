KEYPOINT_COLORS = [
  "#f7fafc",
  "#edf2f7",
  "#e2e8f0",
  "#cbd5e0",
  "#a0aec0",
  "#718096",
  "#4a5568",
  "#2d3748",
  "#1a202c",
  "#f8f0fc",
  "#f3ebff",
  "#e9d8fd",
  "#d6bcfa",
  "#b794f4",
  "#9f7aea",
  "#805ad5",
  "#6b46c1",
  "#553c9a",
  "#e6fffa",
  "#b2f5ea",
  "#81e6d9",
  "#4fd1c5",
  "#38b2ac",
  "#319795"
]

CHART_BACKGROUND_COLOR = '#ffffff'

def hex_to_rgb(hex_string):
    # Remove '#' if present
    if hex_string.startswith('#'):
        hex_string = hex_string[1:]

    # Ensure the hex string is valid
    if len(hex_string) != 6:
        raise ValueError("Invalid hex string length. It should be 6 characters long (excluding '#').")

    # Convert hex to RGB
    r = int(hex_string[0:2], 16)
    g = int(hex_string[2:4], 16)
    b = int(hex_string[4:6], 16)
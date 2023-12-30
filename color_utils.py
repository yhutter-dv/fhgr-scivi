KEYPOINT_COLORS = [
    '#F92672', '#66D9EF', '#A6E22E', '#FD971F', '#E6DB74', '#AE81FF',
    '#66FF66', '#FF99CC', '#FFB366', '#99CCFF', '#66CCCC', '#FF6666',
    '#6699FF', '#CC99FF', '#C6E2FF', '#FFCCCC', '#A8FF60', '#FFE666',
    '#C6FFDD', '#E1F5C4', '#FF80AB', '#B19CD9', '#FF91AF', '#A8FF60'
]

CHART_BACKGROUND_COLOR = '#272822'

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
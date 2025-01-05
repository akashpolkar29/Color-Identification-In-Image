import cv2
import pandas as pd

# File paths
img_path = r"E:\Projects\Color Identification in Images\Image.jpg"
csv_path = r"E:\Projects\Color Identification in Images\colors (1).csv"

# Reading the CSV file and creating a dataframe
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# Reading the image and resizing it
img = cv2.imread(img_path)
img = cv2.resize(img, (800, 600))

# Global variables
clicked = False
r = g = b = xpos = ypos = 0

# Function to get color name based on RGB values
def get_color_name(R, G, B):
    minimum = 1000
    cname = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d < minimum:
            minimum = d
            cname = df.loc[i, 'color_name']
    return cname

# Function to get RGB values on double-click
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Set up the OpenCV window and mouse callback
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', draw_function)

while True:
    cv2.imshow('Image', img)
    if clicked:
        # Draw a filled rectangle to display the color name
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Generate the text to display
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        
        # Display the text with suitable color for readability
        cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255) if r + g + b < 600 else (0, 0, 0), 2, cv2.LINE_AA)
        
        # Reset clicked to allow further clicks
        clicked = False

    # Break loop when 'ESC' key is pressed
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()

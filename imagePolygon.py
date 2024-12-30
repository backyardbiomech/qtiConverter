import cv2
import matplotlib.pyplot as plt
import numpy as np

# Initialize global variables
points = []
polygon_closed = False

def click_event(event, x, y, flags, param):
    global points, polygon_closed

    if event == cv2.EVENT_LBUTTONDOWN:
        if polygon_closed:
            return
        points.append((x, y))
        if len(points) > 1:
            cv2.line(img, points[-2], points[-1], (0, 255, 0), 2)
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow('image', img)

    elif event == cv2.EVENT_LBUTTONDBLCLK:
        if len(points) > 2:
            cv2.line(img, points[-1], points[0], (0, 255, 0), 2)
            polygon_closed = True
            cv2.imshow('image', img)

def main():
    global img

    # Ask for the image path
    image_path = input("Enter the path to the image: ")

    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print("Could not open or find the image.")
        return

    # Display the image
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)

    # Wait until the user presses a key
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Calculate the coordinates as percentages
    height, width, _ = img.shape
    percent_coords = [(x / width, y / height) for x, y in points]

    # Print the coordinates
    print("Polygon vertices (as percentages of width and height):")
    for coord in percent_coords:
        print(coord)

if __name__ == "__main__":
    main()
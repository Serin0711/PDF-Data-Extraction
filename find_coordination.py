import cv2
import numpy as np


def find_roi_coordinates(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to get binary image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize a list to store ROI coordinates
    roi_coordinates = []

    # Loop through the contours and extract ROI coordinates
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Filter out small contours (noise)
        if w > 10 and h > 10:
            roi_coordinates.append((x, y, x + w, y + h))  # (x1, y1, x2, y2)
            # Draw rectangle around the detected ROI
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Save the output image with rectangles drawn around ROIs
    output_image_path = "image/04.jpg"
    cv2.imwrite(output_image_path, image)

    return roi_coordinates, output_image_path


# Example usage
image_path = "image/04.jpg"
roi_coordinates, output_image_path = find_roi_coordinates(image_path)

# Print the detected ROI coordinates
print("ROI Coordinates:")
for roi in roi_coordinates:
    print(roi,",")

# Display the output image with rectangles drawn around ROIs
cv2.imshow("Detected ROIs", cv2.imread(output_image_path))
cv2.waitKey(0)
cv2.destroyAllWindows()

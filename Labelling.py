import cv2
import os
import csv

# Global variables
points = []
image_label = ""

# Function to check if the image has already been processed
def load_processed_images(output_file):
    processed_images = set()
    if os.path.exists(output_file):
        with open(output_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                processed_images.add(row[0])  # Add the filename to the set
    return processed_images

def click_event(event, x, y, flags, param):
    global points
    img = param
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 11:
            points.append((x, y))
            # Display the point and coordinates on the image
            cv2.circle(img, (x, y), 3, (0, 0, 255), -1)  # Draw a red dot for the point
            cv2.putText(img, f"({x},{y})", (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)  # Show coordinates
            cv2.imshow("Image", img)
        else:
            print("Already captured 11 points. Press 'Enter' to confirm or 'Backspace' to reset.")

def reset_points(img):
    global points
    points = []
    cv2.imshow("Image", img)

def process_images(image_folder, output_file):
    global image_label
    
    # Load the images that have already been processed
    processed_images = load_processed_images(output_file)

    # Open the CSV file in append mode
    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write header only if the file is new
        if os.stat(output_file).st_size == 0:
            writer.writerow(['Filename', 'Label', 'Point1_x', 'Point1_y', 'Point2_x', 'Point2_y', 'Point3_x', 'Point3_y',
                             'Point4_x', 'Point4_y', 'Point5_x', 'Point5_y', 'Point6_x', 'Point6_y', 'Point7_x', 'Point7_y',
                             'Point8_x', 'Point8_y', 'Point9_x', 'Point9_y', 'Point10_x', 'Point10_y', 'Point11_x', 'Point11_y'])

        # Sort the image filenames for ordered processing
        filenames = sorted([f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg"))])

        # Iterate through sorted images
        for filename in filenames:
            if filename in processed_images:
                print(f"Skipping already processed image: {filename}")
                continue
            
            img_path = os.path.join(image_folder, filename)
            img = cv2.imread(img_path)
            
            # Check if image is loaded properly
            if img is None:
                print(f"Error loading image: {img_path}")
                continue
            else:
                print(f"Successfully loaded image: {filename}")
            
            img_copy = img.copy()

            # Show the image before asking for the label
            reset_points(img_copy)
            cv2.imshow("Image", img_copy)
            cv2.waitKey(1)  # Ensures the window is rendered

            # Ask for the label while the image is displayed
            while True:
                image_label = input(f"Enter the 11-character label for {filename}: ")
                if len(image_label) == 11:
                    break
                else:
                    print("Label must be exactly 11 characters. Please try again.")

            # Start collecting points with the label confirmed
            print("Click center for all characters, press backspace to reset or enter to confirm once all 11 characters have been clicked")
            cv2.setMouseCallback("Image", click_event, img_copy)

            # Wait for the user to press 'Enter' or 'Backspace'
            while True:
                key = cv2.waitKey(1) & 0xFF
                if key == 13:  # 'Enter' key
                    if len(points) == 11:
                        break
                    else:
                        print("Please select 11 points before confirming.")
                elif key == 8:  # 'Backspace' key
                    reset_points(img_copy)
            
            # Save the points and label to CSV
            if len(points) == 11:
                row = [filename, image_label] + [coord for point in points for coord in point]
                writer.writerow(row)
                print(f"Data saved for {filename}")
            else:
                print(f"Data not saved for {filename}, incorrect number of points.")
                
    print(f"All data has been saved to {output_file}")
    cv2.destroyAllWindows()

# Provide the path to your images folder and CSV file
image_folder = 'Group project/to_label'
output_file = 'output_labels_and_coordinates.csv'

process_images(image_folder, output_file)

import cv2
import csv
import os

def draw_annotations(image_folder, csv_file, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Open the CSV file and read annotations
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header row

        # Iterate through each row in the CSV
        for row in reader:
            filename = row[0]
            label = row[1]
            coordinates = row[2:]  # All points after the label

            # Load the image
            img_path = os.path.join(image_folder, filename)
            img = cv2.imread(img_path)

            if img is None:
                print(f"Error loading image: {img_path}")
                continue
            
            # Draw each point on the image
            for i in range(0, len(coordinates), 2):
                x = int(coordinates[i])
                y = int(coordinates[i + 1])
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)  # Red dot for each point

            # Write the label at the top center of the image
            label_position = (10, 30)  # Adjust as needed for position
            cv2.putText(img, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Save the annotated image in the output folder
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, img)
            print(f"Annotated image saved: {output_path}")

# Paths for image folder, CSV file, and output folder
image_folder = './theo_images'
csv_file = 'output_labels_and_coordinates.csv'
output_folder = './output' #Folder to store the annotated images

# Run the annotation drawing function
draw_annotations(image_folder, csv_file, output_folder)

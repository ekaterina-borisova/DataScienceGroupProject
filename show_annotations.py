import cv2
import csv
import os

def draw_annotations(image_folder, csv_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            filename = row[0]
            label = row[1]
            coordinates = row[2:]

            img_path = os.path.join(image_folder, filename)
            img = cv2.imread(img_path)

            if img is None:
                print(f"Error loading image: {img_path}")
                continue
            
            for i in range(0, len(coordinates), 2):
                x = int(coordinates[i])
                y = int(coordinates[i + 1])
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

            label_position = (10, 30)
            cv2.putText(img, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, img)
            print(f"Annotated image saved: {output_path}")


image_folder = './theo_images'
csv_file = 'output_labels_and_coordinates.csv'
output_folder = './output' 

draw_annotations(image_folder, csv_file, output_folder)

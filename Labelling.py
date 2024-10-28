import cv2
import os
import csv

points = []
image_label = ""


def load_processed_images(output_file):
    processed_images = set()
    if os.path.exists(output_file):
        with open(output_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                processed_images.add(row[0])
    return processed_images

def click_event(event, x, y, flags, param):
    global points
    img = param
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 11:
            points.append((x, y))
            
            cv2.circle(img, (x, y), 3, (0, 0, 255), -1) 
            cv2.putText(img, f"({x},{y})", (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.imshow("Image", img)
        else:
            print("Already captured 11 points. Press 'Enter' to confirm or 'Backspace' to reset.")

def reset_points(img):
    global points
    points = []
    cv2.imshow("Image", img)

def process_images(image_folder, output_file):
    global image_label
    
    processed_images = load_processed_images(output_file)

    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if os.stat(output_file).st_size == 0:
            writer.writerow(['Filename', 'Label', 'Point1_x', 'Point1_y', 'Point2_x', 'Point2_y', 'Point3_x', 'Point3_y',
                             'Point4_x', 'Point4_y', 'Point5_x', 'Point5_y', 'Point6_x', 'Point6_y', 'Point7_x', 'Point7_y',
                             'Point8_x', 'Point8_y', 'Point9_x', 'Point9_y', 'Point10_x', 'Point10_y', 'Point11_x', 'Point11_y'])

        filenames = sorted([f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg"))])

        for filename in filenames:
            if filename in processed_images:
                print(f"Skipping already processed image: {filename}")
                continue
            
            img_path = os.path.join(image_folder, filename)
            img = cv2.imread(img_path)
            
            if img is None:
                print(f"Error loading image: {img_path}")
                continue
            else:
                print(f"Successfully loaded image: {filename}")
            
            img_copy = img.copy()

            
            reset_points(img_copy)
            cv2.imshow("Image", img_copy)
            cv2.waitKey(1) 

            while True:
                image_label = input(f"Enter the 11-character label for {filename}: ")
                if len(image_label) == 11:
                    break
                else:
                    print("Label must be exactly 11 characters. Please try again.")

            print("Click center for all characters, press backspace to reset or enter to confirm once all 11 characters have been clicked")
            cv2.setMouseCallback("Image", click_event, img_copy)

            while True:
                key = cv2.waitKey(1) & 0xFF
                if key == 13:  # Enter key
                    if len(points) == 11:
                        break
                    else:
                        print("Please select 11 points before confirming.")
                elif key == 8:  # Backspace key
                    reset_points(img_copy)
            
            
            if len(points) == 11:
                row = [filename, image_label] + [coord for point in points for coord in point]
                writer.writerow(row)
                print(f"Data saved for {filename}")
            else:
                print(f"Data not saved for {filename}, incorrect number of points.")
                
    print(f"All data has been saved to {output_file}")
    cv2.destroyAllWindows()

image_folder = 'Group project/to_label'
output_file = 'output_labels_and_coordinates.csv'

process_images(image_folder, output_file)

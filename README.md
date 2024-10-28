# Data Science Group Project

##Annotation Script
This script allows users to manually annotate images by entering the label of the image and then selecting 11 points on each image. The points and labels are saved to a CSV file.

Steps:

1. Input Image Folder: Update image_folder to the directory containing the images.
2. CSV Output: Update output_file to specify where to save annotations.
3. Annotations:
    - The script displays each image sequentially.
    - Enter a label (11 characters).
    - Click on 11 points within the image.
    - Press Enter to save or Backspace to reset points for the current image.

##Visualize Annotation Script
This script reads the a csv file of the labels and points to then superimpose the saved points and write the label onto each corresponding image.

Steps:
1. Image Folder: Update image_folder to the directory containing the images.
2. CSV File: Ensure csv_file points to the directory containg the csv file with the points and labels.
3. Output Folder: Update output_folder to specify where to save annotated images.

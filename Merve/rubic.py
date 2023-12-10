from torchvision import transforms
from PIL import Image
import numpy as np
import csv
import os
image_folder = "/home/merve/Desktop/rubic/"
output_csv_path = '/home/merve/Desktop/colors.csv'
with open(output_csv_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Filename', 'R', 'G', 'B','Color'])
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg"):  
            img_path = os.path.join(image_folder, filename)
            rgb_image = Image.open(img_path).convert("RGB")
            rgb_tensor = transforms.ToTensor()(rgb_image)
            grayscale_tensor = transforms.functional.rgb_to_grayscale(rgb_tensor)
            grayscale_array = np.array(grayscale_tensor[0])
            hist, bins = np.histogram(grayscale_array, bins=256, range=[0, 1])
            top_pixel_values = np.argsort(hist)[-9:][::-1]
            for pixel_index, (x, y) in enumerate(zip([pixel % rgb_image.width for pixel in top_pixel_values],
                                                     [pixel // rgb_image.width for pixel in top_pixel_values])):
                rgb_values = rgb_image.getpixel((x, y))
                csv_writer.writerow([filename] + list(rgb_values) + [''])
print(f"CSV dosyası oluşturuldu: {output_csv_path}")

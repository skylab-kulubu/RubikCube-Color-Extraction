from sklearn.metrics.pairwise import cosine_similarity
from itertools import combinations
from torchvision import transforms
from PIL import Image
import csv
csv_file_path = '/home/merve/Desktop/colors.csv'
data = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)
    for row in csv_reader:
        data.append(row)
rgb_data = [(int(row[1]), int(row[2]), int(row[3])) for row in data]
new_image_path = '/home/merve/Desktop/example.jpg'
new_image = Image.open(new_image_path).convert("RGB")
new_image_tensor = transforms.ToTensor()(new_image)
new_image_rgb = (int(new_image_tensor[0][0][0].item() * 255),
                 int(new_image_tensor[0][0][1].item() * 255),
                 int(new_image_tensor[0][0][2].item() * 255))
rgb_data.append(new_image_rgb)
similar_rows = []
for pair in combinations(range(len(data)), 2):
    similarity = cosine_similarity([rgb_data[pair[0]]], [rgb_data[pair[1]]])[0][0]
    similar_rows.append((pair[0], pair[1], similarity))
similar_rows = sorted(similar_rows, key=lambda x: x[2], reverse=True)
selected_rows = set()
for row1, row2, similarity in similar_rows:
    selected_rows.add(row1)
    selected_rows.add(row2)
    if len(selected_rows) >= 9:
        break
print("En benzeyen 9 satırın RGB renkleri:")
for row_index in selected_rows:
    print(rgb_data[row_index])

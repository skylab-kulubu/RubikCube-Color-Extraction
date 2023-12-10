import numpy as np
from torchvision import transforms
from PIL import Image
img_path = "/home/merve/Desktop/example.jpg"
rgb_image = Image.open(img_path).convert("RGB")
rgb_tensor = transforms.ToTensor()(rgb_image)
grayscale_tensor = transforms.functional.rgb_to_grayscale(rgb_tensor)
grayscale_image = transforms.ToPILImage()(grayscale_tensor)
grayscale_array = np.array(grayscale_tensor[0])
hist, bins = np.histogram(grayscale_array, bins=256, range=[0, 1])
top_pixel_values = np.argsort(hist)[-9:][::-1]
rgb_values = [rgb_image.getpixel((x, y)) for x, y in zip([100, 100, 100, 150, 150, 150, 200, 200, 200], [100, 150, 200] * 3)]
print("En çok kullanılan 9 piksel değeri:", top_pixel_values)
print("Bu piksel değerlerinin RGB karşılıkları:", rgb_values)

# Bu kod foto'ya 3x3'lük grid çizerek oluşan karelerin merkezlerine küçük yuvarlaklar çiziyo ve sadece o alanlar için maske oluşturuyo. Bu sayede background kodu
# pek etkilemiyo. Ayrıca kare merkezlerinin küpten uzak olmaması için fotoları kare değillerse kare olucak şekilde kırpıyor.

# Filtreleme yaparken de rengin yüzdesine bakıyo ki küçük parlamalar engellensin.

# Yine de küp foto merkezinden çok kayık olmazsa güzel olur.

import cv2
import numpy as np

def detect_colors(image_path):

    im = cv2.imread(image_path)

    h, w, _ = im.shape

    ratio = h / w

    if(abs(h - w) > 75):
        if ratio > 1:
            crop_size = int((h - w) / 2)
            image = im[crop_size:h-crop_size, :]
        elif ratio < 1:
            crop_size = int((w - h) / 2)
            image = im[:, crop_size:w-crop_size]
    else:
        image = im

    #cv2.imshow("image", image)
    #cv2.waitKey(0)

    height, width, _ = image.shape
    image_area = height * width
    radius = int(np.sqrt(image_area) * 0.02)

    centers = []
    for i in range(3):
        for j in range(3):
            cX = int((i + 0.5) * width / 3)
            cY = int((j + 0.5) * height / 3)
            centers.append((cX, cY))

    lower_bounds = {
        'red': np.array([0, 120, 50]),
        'red2': np.array([176, 120, 70]),
        'green': np.array([45, 40, 40]),
        'blue': np.array([95, 100, 50]),
        'yellow': np.array([20, 100, 100]),
        'orange': np.array([4, 150, 100]),
        'pink': np.array([152, 100, 100]),
        'white': np.array([0, 0, 100])
    }

    upper_bounds = {
        'red': np.array([3, 255, 255]),
        'red2': np.array([180, 255, 255]),
        'green': np.array([85, 255, 255]),
        'blue': np.array([120, 255, 255]),
        'yellow': np.array([44, 255, 255]),
        'orange': np.array([19, 255, 255]),
        'pink': np.array([165, 255, 255]),
        'white': np.array([180, 99, 255])
    }

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    results = []

    for color, lower_bound in lower_bounds.items():
        for square, center in enumerate(centers, 1):
            upper_bound = upper_bounds[color]

            mask = np.zeros_like(hsv_image)
            cv2.circle(mask, center, radius, (255, 255, 255), -1)
            and_image = cv2.bitwise_and(hsv_image, mask)
            #cv2.imshow("and_image", cv2.cvtColor(cv2.resize(and_image, (800, 600)), cv2.COLOR_HSV2BGR))
            #cv2.waitKey(0)

            color_mask = cv2.inRange(and_image, lower_bound, upper_bound)

            total_area = np.sum(mask // 255)
            color_area = np.sum(color_mask // 255)
            area_percentage = (color_area / total_area) * 100 # tamamı yüzde 33.33'e denk geliyor

            if area_percentage >= 16.665: # 33.33'ün yarısı - beyaz renk yansımıştır vs onu da içine almasın diye.
                results.append((square, color)) 
                cv2.putText(image, str(square), (center[0], center[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

    results.sort(key=lambda x: x[0])

    for square, color in results:
        if color == 'red2':
            print(f"Square {square} is red")
        else:
            print(f"Square {square} is {color}")

    resized_image = cv2.resize(image, (600, 600))
    cv2.imshow("Rubik's Cube Squares", resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

detect_colors('pics/nolurcalis.jpg')
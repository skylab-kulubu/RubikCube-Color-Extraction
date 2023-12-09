import cv2
import numpy as np

color_ranges = {
    'Red_1': ([0, 95, 100], [5, 255, 255]),
    'Red_2': ([160, 95, 100], [180, 255, 255]),
    'Orange': ([6, 100, 100], [24, 255, 255]),
    'Yellow': ([25, 100, 100], [39, 255, 255]),
    'Green': ([40, 100, 100], [80, 255, 255]),
    'Blue': ([90, 50, 100], [130, 255, 255]),
    'White': ([0, 0, 200], [180, 50, 255])
}

image = cv2.imread('TestDatas/5.jpg')

image = cv2.resize(image, (300, 300))

for i in range(3):
    for j in range(3):
        x = 50 + i * 100
        y = 50 + j * 100

        square = image[x - 10:x + 10, y - 10:y + 10]
        # cv2.imshow('Square', square)
        # cv2.waitKey(0)

        color_name = 'Unknown'

        for color, (lower, upper) in color_ranges.items():
            lower_bounds = np.array(lower, dtype=np.uint8)
            upper_bounds = np.array(upper, dtype=np.uint8)

            hsv = cv2.cvtColor(square, cv2.COLOR_BGR2HSV)
            # cv2.imshow('Square HSV', hsv)
            # cv2.waitKey(0)

            mask = cv2.inRange(hsv, lower_bounds, upper_bounds)
            # cv2.imshow('Mask', mask)
            # cv2.waitKey(0)

            if cv2.countNonZero(mask) > 0:
                color_name = color
                break

        color_value = square[10, 10]
        color_hsv = np.uint8([[color_value]])
        hsv_value = cv2.cvtColor(color_hsv, cv2.COLOR_BGR2HSV)

        if color_name == 'Red_1' or color_name == 'Red_2':
            print(f'Square {i * 3 + j + 1} : Red')
        else:
            print(f'Square {i * 3 + j + 1} : {color_name}')
            
        print(f'- (B:{color_value[0]}, G:{color_value[1]}, R:{color_value[2]})')
        print(f'- (H:{hsv_value[0][0][0]}, S:{hsv_value[0][0][1]}, V:{hsv_value[0][0][2]})\n')

cv2.imshow("Rubik's Cube", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

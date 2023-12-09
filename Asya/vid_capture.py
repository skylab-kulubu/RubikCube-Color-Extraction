# Foto çekerken küp karelere gelicek şekilde yerleştirerek sadece istediğimiz alanları alıyoruz ve oradaki renkleri belirliyoruz. 

# Parlaklıklar boyut filtrelemesi ile hallediliyor.

import cv2
import numpy as np

def capture_photo():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        draw_squares(frame)
        cv2.imshow('Camera', frame)

        key = cv2.waitKey(1)
        if key == ord('s'):
            image = return_image(frame)
            return image
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def draw_squares(frame):
    global square_coordinates

    square_coordinates = [
        (200, 100), (300, 100), (400, 100),
        (200, 200), (300, 200), (400, 200),
        (200, 300), (300, 300), (400, 300),
    ]

    for coord in square_coordinates:
        cv2.rectangle(frame, (coord[0], coord[1]), (coord[0] + 40, coord[1] + 40), (0, 0, 0), 2)

def return_image(frame):
    black_image = np.zeros_like(frame)

    for coord in square_coordinates:
        x, y = coord
        w, h = 40, 40
        black_image[y:y+h, x:x+w] = frame[y:y+h, x:x+w]

    return black_image

def detect_colors(im):
    image = im

    height, width, _ = image.shape
    image_area = height * width

    lower_bounds = {
        'red': np.array([0, 120, 50]),
        'red2': np.array([176, 120, 70]),
        'green': np.array([45, 40, 40]),
        'blue': np.array([95, 100, 50]),
        'yellow': np.array([20, 100, 100]),
        'orange': np.array([5, 150, 100]),
        'pink': np.array([152, 100, 100]),
        'white': np.array([0, 0, 100])
    }

    upper_bounds = {
        'red': np.array([5, 255, 255]),
        'red2': np.array([180, 255, 255]),
        'green': np.array([85, 255, 255]),
        'blue': np.array([125, 255, 255]),
        'yellow': np.array([44, 255, 255]),
        'orange': np.array([20, 255, 255]),
        'pink': np.array([165, 255, 255]),
        'white': np.array([180, 99, 255])
    }

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    results = []
    centers = []

    for color, lower_bound in lower_bounds.items():
        upper_bound = upper_bounds[color]
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        filtered_contours = []
        
        for contour in contours:
            area_percantage = cv2.contourArea(contour) / image_area

            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2
            
            if area_percantage > 0.004:
                filtered_contours.append(contour)
                centers.append((center_x, center_y))

        for counter, contour in enumerate(filtered_contours, len(results) + 1): 
            if (counter, color) not in results:
                results.append((counter, color))

    results.sort(key=lambda x: x[0])
    
    for (counter, color), (center_x, center_y) in zip(results, centers):
        if color == 'red2':
            print(f"Square {counter} is red")
        else:
            print(f"Square {counter} is {color}") 

        cv2.putText(image, str(counter), (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
    cv2.imshow("Rubik's Cube Squares", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image = capture_photo()
    detect_colors(image)

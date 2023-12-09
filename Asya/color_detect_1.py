# Bu kod color bound'lara göre maskeler oluşturuyo ve bu maskedeki kontürleri buluyo. Bu kontürlerden istediğimiz kare şekillerini ayrıştırmak içinse kontürün hem boyutuna
# hem de h/w oranlarına bakarak küçük kontürleri veya şekilsiz kontürleri filtrelemiş oluyo. 

# Kırpılmış foto kullanılması lazım.

import cv2
import numpy as np

def detect_colors(image_path):
    image = cv2.imread(image_path)

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
            aspect_ratio = float(w)/h if h != 0 else 0     
            aspect_ratio_2 = float(h)/w if w != 0 else 0  

            center_x = x + w // 2
            center_y = y + h // 2   
            
            if (area_percantage > 0.03) and (aspect_ratio < 1.3) and (aspect_ratio_2 < 1.3):
                filtered_contours.append(contour)
                centers.append((center_x, center_y))
    
        for counter, contour in enumerate(filtered_contours, len(results) + 1):
            if (counter, color) not in results:
                results.append((counter, color))
                cv2.drawContours(image, [contour], -1, (255, 255, 0), 2)

    results.sort(key=lambda x: x[0])
    
    for (counter, color), (center_x, center_y) in zip(results, centers):
        if color == 'red2':
            print(f"Square {counter} is red")
        else:
            print(f"Square {counter} is {color}")  
        
        cv2.putText(image, str(counter), (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
         
    resized_image = cv2.resize(image, (600, 600))
    cv2.imshow("Rubik's Cube Squares", resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()        

detect_colors('mypics/img_15.jpg')

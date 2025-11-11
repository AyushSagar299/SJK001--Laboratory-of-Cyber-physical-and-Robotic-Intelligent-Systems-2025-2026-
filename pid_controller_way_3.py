import WebGUI
import HAL
import cv2
import numpy as np

Kp = 0.003
Ki = 0.00001
Kd = 0.0014
W_max = 0.9

prev_err = 0
sum_err = 0
last_dir = 1
filtered_err = 0
alpha = 0.85
i = 0

lost_counter = 0
lost_limit = 5

roi_y_start = 0.6  

while True:
    img = HAL.getImage()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    red_mask = cv2.bitwise_or(
        cv2.inRange(hsv, (0, 120, 100), (10, 255, 255)),
        cv2.inRange(hsv, (160, 120, 100), (180, 255, 255))
    )

    h, w = red_mask.shape
    roi = red_mask[int(h * roi_y_start):, :]  

    contours, _ = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    line_found = False
    if contours:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > 150:
            M = cv2.moments(c)
            if M["m00"] > 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"]) + int(h * roi_y_start)  
                line_found = True

    if line_found:
        lost_counter = 0
        
        err = (w // 2) - cX
        filtered_err = alpha * filtered_err + (1 - alpha) * err  
        d_err = filtered_err - prev_err
        sum_err = 0.9 * sum_err + filtered_err  

        control = Kp * filtered_err + Ki * sum_err + Kd * d_err
        control = np.clip(control, -W_max, W_max)

        v = 3.2 - min(abs(filtered_err) / 60, 2.0)
        v = np.clip(v, 1.5, 3.2)

        HAL.setV(v)
        HAL.setW(control)

        prev_err = filtered_err
        last_dir = 1 if filtered_err > 0 else -1

    else:
        lost_counter += 1

        if lost_counter < lost_limit:
            HAL.setV(1.5)
            HAL.setW(0.3 * last_dir)
        else:
            HAL.setV(1.0)
            HAL.setW(0.6 * last_dir)
            if lost_counter % 25 == 0:
                last_dir *= -1  
    WebGUI.showImage(red_mask)

    print(f"{i:04d} | found:{line_found} | err:{filtered_err:.1f} | lost:{lost_counter}")
    
    i += 1

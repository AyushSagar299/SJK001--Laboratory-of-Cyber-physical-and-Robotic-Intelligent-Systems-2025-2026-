# SJK001--Laboratory-of-Cyber-physical-and-Robotic-Intelligent-Systems-2025-2026-
Labortory Work

**P Controller**

This controller uses only the proportional term to guide the car. In my code, the camera detects a red line using an HSV mask, and the centroid of the line is calculated. The error is found by subtracting the line’s position from the image center. The steering (W) is then adjusted by multiplying this error with a proportional constant (Kp). By tuning this constant, the car follows the line smoothly without too much oscillation or delay.

**PD Controller**

In this code, I have added a derivative term to improve stability. Along with the proportional error, the rate of change of error is calculated using the difference between the current and previous errors. The final control signal is the sum of both terms (Kp * err + Kd * d_err). This helps reduce overshoot and allows the car to follow the line more smoothly and accurately, especially around turns.

**PID Controller**

This is the complete controller combining proportional, integral, and derivative terms. In my file, I calculate the filtered error, the accumulated (integral) error, and the change in error. These three are used together to adjust the car’s angular velocity for smoother line tracking. The speed (V) is also varied depending on how large the error is — slower during turns and faster on straight paths. By tuning Kp, Ki, and Kd, the car follows the path precisely and remains stable.


### Submitted Files

- **`p_controller_way_1.py`**  
    This file contains the implementation of the Proportional (P) Controller.  
    The car detects a red line using an HSV mask, and the centroid of the line is calculated.  
    The steering angle is adjusted based on the difference between the line’s position and the center of the image.  
    By tuning the proportional gain `Kp`, the car can follow the line smoothly without much oscillation or delay.

- **`pd_controller_way_2.py`**  
    This file includes the Proportional-Derivative (PD) Controller.  
    It adds a derivative term to improve stability and reduce oscillations.  
    Along with the proportional error, the change in error is also calculated to make smoother corrections,  
    especially while turning. The combination of `Kp` and `Kd` helps the car maintain a steady and accurate path.

- **`pid_controller_way_3.py`**  
    This file implements the complete Proportional-Integral-Derivative (PID) Controller.  
    It combines all three control terms — proportional, integral, and derivative — for more precise control.  
    The integral term helps to remove accumulated errors, while the derivative term prevents overshoot.  
    The speed of the car is also adjusted depending on how large the error is,  
    making it slower during turns and faster on straight paths.  
    By tuning `Kp`, `Ki`, and `Kd`, the car can follow the line smoothly and remain stable in all conditions.

### Conclusion
Each controller improves upon the previous one.  
The **P Controller** provides basic control, the **PD Controller** adds stability,  
and the **PID Controller** achieves precise and smooth line following performance.


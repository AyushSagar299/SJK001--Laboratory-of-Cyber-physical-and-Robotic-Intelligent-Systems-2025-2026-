# SJK001--Laboratory-of-Cyber-physical-and-Robotic-Intelligent-Systems-2025-2026-
Labortory Work

**P Controller**

This controller uses only the proportional term to guide the car. In my code, the camera detects a red line using an HSV mask, and the centroid of the line is calculated. The error is found by subtracting the line’s position from the image center. The steering (W) is then adjusted by multiplying this error with a proportional constant (Kp). By tuning this constant, the car follows the line smoothly without too much oscillation or delay.

**PD Controller**

In this code, I have added a derivative term to improve stability. Along with the proportional error, the rate of change of error is calculated using the difference between the current and previous errors. The final control signal is the sum of both terms (Kp * err + Kd * d_err). This helps reduce overshoot and allows the car to follow the line more smoothly and accurately, especially around turns.

**PID Controller**

This is the complete controller combining proportional, integral, and derivative terms. In my file, I calculate the filtered error, the accumulated (integral) error, and the change in error. These three are used together to adjust the car’s angular velocity for smoother line tracking. The speed (V) is also varied depending on how large the error is — slower during turns and faster on straight paths. By tuning Kp, Ki, and Kd, the car follows the path precisely and remains stable.

# Autonomous Drone Search and Rescue System

## Overview

This project implements a **Python-based autonomous drone control system** designed for search and rescue scenarios. The drone operates autonomously by following a **spiral search pattern** and using **computer vision-based face detection** to identify potential victims.

The mission workflow is fully automated: the drone takes off, navigates to a predefined search center, performs a spiral search while analyzing camera images, records detected victims, and finally returns and lands safely.

The system integrates **finite state machine control**, **motion control**, and **OpenCV-based visual detection** to ensure reliable and structured autonomous behavior.

---

## Initialization and Configuration

At startup, the program defines the key mission parameters, including the center of the search area, the desired flight altitude, spiral motion characteristics such as growth rate and velocity, and the maximum number of victims to be detected.

The face detection module is initialized using OpenCV’s **Haar Cascade classifier**, which processes images from the drone’s downward-facing camera to identify potential victims.

---

## Mission Control Logic

The mission is managed using a **Finite State Machine (FSM)**, which ensures clear transitions and predictable behavior throughout the operation. The drone progresses through multiple phases, starting with takeoff and ascent, followed by navigation to the search center. Once the center is reached, the drone begins the search operation. After completing the search, a mission report is generated, and the drone returns to the origin and lands.

This structured approach improves safety, readability, and maintainability.

---

## Time-Based Motion Control

The system continuously measures the elapsed time between control cycles. This timing information is used to update movement commands smoothly, ensuring stable flight behavior and consistent spiral motion even under varying execution timings.

---

## Computer Vision and Victim Detection

During flight, the drone continuously captures images from its ventral (downward-facing) camera. Each image is converted to grayscale and analyzed at multiple orientations to improve robustness against different face angles.

When a face is detected, the system highlights the detection and records the drone’s current position as a victim location. To prevent duplicate detections, the system verifies that the new detection is sufficiently distant from previously recorded victims before registering it.

---

## Navigation and Search Strategy

The drone uses proportional control to navigate toward the center of the search area. Once there, it follows an **Archimedean spiral trajectory**, which gradually expands outward.

The spiral parameters are designed to maintain a stable tangential speed while ensuring efficient and systematic area coverage.

---

## Mission Completion

The search continues until the maximum number of victims has been detected. Afterward, the system generates a mission summary listing the number and estimated positions of detected victims.

The drone then navigates back to the origin while maintaining altitude and performs a controlled landing to safely conclude the mission.

---

## Key Techniques Used

- Finite State Machine (FSM) for mission sequencing  
- Proportional control for navigation and altitude regulation  
- Archimedean spiral path planning for area coverage  
- OpenCV Haar Cascade for face detection  
- Real-time image processing and sensor feedback  

---

## Summary

This project demonstrates a complete autonomous search-and-detection workflow by integrating drone control, trajectory planning, and computer vision in a clear and structured manner. It is suitable for simulation environments and can be adapted to real robotic platforms that provide camera input and motion control interfaces.

import cv2
import numpy as np
import math
import time
import WebGUI as GUI
import HAL

# Mission Parameters

# Spiral center (world coordinates)
CENTER_X = 33.0
CENTER_Y = -35.0

# Flight altitude
ALTITUDE = 4.0

# Spiral parameters
SPIRAL_VELOCITY = 2.0      # Tangential velocity (m/s)
SPIRAL_GROWTH = 0.2        # Spiral growth factor
MAX_VICTIMS = 6.0          # Max victims to detect

# Spiral State

spiral_angle = 0.0         # Accumulated spiral angle
current_radius = 0.0       # Current spiral radius


# Face Detection Setup

cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)


# Mission State

state = "TAKEOFF"
found_victims = []
last_time = time.time()


# Utility Functions

def rotate_image_gray(gray_img, angle_deg):
    """
    Rotate a grayscale image by a given angle.
    """
    h, w = gray_img.shape[:2]
    center = (w / 2, h / 2)
    rot_mat = cv2.getRotationMatrix2D(center, angle_deg, 1.0)
    return cv2.warpAffine(gray_img, rot_mat, (w, h), flags=cv2.INTER_LINEAR)


# Mission Start

print(f"Misión: Espiral centrada en [{CENTER_X}, {CENTER_Y}]")


while True:

    # ---- Time step ----
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    if dt <= 0:
        dt = 0.01

    # ---- Sensor data ----
    img = HAL.get_ventral_image()
    if img is None:
        continue

    current_x, current_y, current_z = HAL.get_position()

    # FACE DETECTION

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_detected = False

    # Try rotated images every 30 degrees
    for angle in range(0, 360, 30):
        if angle == 0:
            check_img = gray
        else:
            check_img = rotate_image_gray(gray, angle)

        faces = face_cascade.detectMultiScale(check_img, 1.2, 3)
        if len(faces) > 0:
            face_detected = True
            break

    # If face detected, mark and register victim
    if face_detected:
        h, w = img.shape[:2]
        cv2.circle(img, (int(w / 2), int(h / 2)), 30, (0, 255, 0), 3)

        if state == "SEARCH":
            is_new_victim = True
            for vx, vy in found_victims:
                dist = math.sqrt((current_x - vx) * 2 + (current_y - vy) * 2)
                if dist < 4.0:
                    is_new_victim = False
                    break

            if is_new_victim:
                print(f"¡VÍCTIMA! Posición: ({current_x:.2f}, {current_y:.2f})")
                found_victims.append([current_x, current_y])

    GUI.showImage(img)

    # STATE MACHINE

    # ---- TAKEOFF ----
    if state == "TAKEOFF":
        HAL.takeoff()

        if current_z < (ALTITUDE - 0.2):
            HAL.set_cmd_vel(0, 0, 1.5, 0)
        else:
            state = "TRAVEL"

    # ---- GO TO CENTER ----
    elif state == "TRAVEL":
        dx = CENTER_X - current_x
        dy = CENTER_Y - current_y
        dist = math.sqrt(dx * 2 + dy * 2)
        hold_z = (ALTITUDE - current_z) * 0.5

        if dist < 1.0:
            print("Centro alcanzado. INICIANDO ESPIRAL.")
            HAL.set_cmd_vel(0, 0, 0, 0)
            state = "SEARCH"
        else:
            vx = max(min(dx * 0.5, 3.0), -3.0)
            vy = max(min(dy * 0.5, 3.0), -3.0)
            HAL.set_cmd_vel(vx, vy, hold_z, 0)

    # ---- SPIRAL SEARCH ----
    elif state == "SEARCH":

        current_radius = SPIRAL_GROWTH * spiral_angle

        if len(found_victims) >= MAX_VICTIMS:
            HAL.set_cmd_vel(0, 0, 0, 0)
            state = "FINISHED"
            continue

        if current_radius < 0.1:
            current_radius = 0.1

        omega = SPIRAL_VELOCITY / current_radius
        spiral_angle += omega * dt

        target_x = CENTER_X + current_radius * math.cos(spiral_angle)
        target_y = CENTER_Y + current_radius * math.sin(spiral_angle)

        error_x = target_x - current_x
        error_y = target_y - current_y

        vx = max(min(error_x * 1.0, 2.5), -2.5)
        vy = max(min(error_y * 1.0, 2.5), -2.5)
        hold_z = (ALTITUDE - current_z) * 0.5

        HAL.set_cmd_vel(vx, vy, hold_z, 0)

    # ---- REPORT ----
    elif state == "FINISHED":
        print("       INFORME DE MISIÓN       ")
        print(f"Víctimas encontradas: {len(found_victims)}")
        print("-" * 40)

        for i, (vx, vy) in enumerate(found_victims, start=1):
            print(f" [{i}] X={vx:.2f}, Y={vy:.2f}")

        print("Volviendo a casa...")
        HAL.set_cmd_pos(0, 0, ALTITUDE, 0)
        state = "LANDING"

    # ---- LAND ----
    elif state == "LANDING":
        dist_home = math.sqrt(current_x * 2 + current_y * 2)

        if dist_home < 1.0:
            HAL.land()
            print("Dron en tierra. Fin del programa.")
            break

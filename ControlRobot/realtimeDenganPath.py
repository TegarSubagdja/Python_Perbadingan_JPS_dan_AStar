import cv2
import numpy as np
from cv2 import aruco
import pygame
import math
import threading

# Initialize webcam and get its dimensions
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if not ret:
    print("Failed to read from webcam.")
    exit()

# Get webcam size
FRAME_WIDTH, FRAME_HEIGHT = frame.shape[1], frame.shape[0]
print(f"Webcam resolution: {FRAME_WIDTH}x{FRAME_HEIGHT}")

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))
pygame.display.set_caption("ArUco Path Tracking")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Variables
path_points = []
robot_pos = [FRAME_WIDTH // 2, FRAME_HEIGHT // 2]
robot_angle = 0
current_target_index = 0
marker_detected = False
font = pygame.font.Font(None, 24)

# Target switching parameters
TARGET_REACHED_DISTANCE = 30  # Distance threshold to consider target reached (in pixels)

# Function to calculate angle between two points
def calculate_angle(p1, p2):
    return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))

# Function to calculate distance between two points
def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Thread function for ArUco detection
def aruco_thread():
    global robot_pos, robot_angle, marker_detected
    
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Flip the frame horizontally to handle mirror effect
        frame_display = cv2.flip(frame, 1)
            
        # Convert to grayscale for detection (use original unflipped frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect markers
        corners, ids, _ = detector.detectMarkers(gray)
        
        marker_detected = False
        if ids is not None:
            # Draw detected markers on the display frame
            corners_display = []
            for corner in corners:
                mirrored_corner = corner.copy()
                mirrored_corner[0, :, 0] = FRAME_WIDTH - mirrored_corner[0, :, 0]
                corners_display.append(mirrored_corner)
            
            aruco.drawDetectedMarkers(frame_display, corners_display, ids)
            
            # Process only the first detected marker
            marker_corners = corners[0][0]
            
            # Calculate marker position (center)
            center_x = int(np.mean([c[0] for c in marker_corners]))
            center_y = int(np.mean([c[1] for c in marker_corners]))
            
            # Mirror the x-coordinate for pygame
            mirrored_center_x = FRAME_WIDTH - center_x
            
            # Update robot position
            robot_pos[0] = mirrored_center_x
            robot_pos[1] = center_y
            
            # Calculate marker orientation
            front_mid_x = (marker_corners[0][0] + marker_corners[1][0]) / 2
            front_mid_y = (marker_corners[0][1] + marker_corners[1][1]) / 2
            
            # Calculate angle from center to front midpoint
            dx = front_mid_x - center_x
            dy = front_mid_y - center_y
            
            # Mirror the angle calculation
            robot_angle = math.degrees(math.atan2(dy, -dx))
            
            marker_detected = True
            
            # Draw orientation line on the display frame
            mirrored_front_x = FRAME_WIDTH - front_mid_x
            cv2.line(frame_display, 
                    (int(mirrored_center_x), int(center_y)), 
                    (int(mirrored_center_x + 30 * math.cos(math.radians(robot_angle))), 
                     int(center_y + 30 * math.sin(math.radians(robot_angle)))), 
                    (0, 255, 0), 2)
        
        # Show camera feed with detections
        cv2.imshow('ArUco Detection', frame_display)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Start ArUco detection in a separate thread
aruco_thread = threading.Thread(target=aruco_thread, daemon=True)
aruco_thread.start()

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            path_points.append(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:  # Clear path
            path_points = []
            current_target_index = 0
    
    # Clear screen
    screen.fill(WHITE)
    
    # Process path and handle target switching
    if path_points and marker_detected:
        # Check if we've reached the current target
        if current_target_index < len(path_points):
            current_target = path_points[current_target_index]
            distance = calculate_distance(robot_pos, current_target)
            
            # If reached the target, move to next target
            if distance <= TARGET_REACHED_DISTANCE:
                current_target_index += 1
                # Play a sound to indicate target reached
                if current_target_index < len(path_points):
                    pygame.mixer.Sound.play(pygame.mixer.Sound(b'\x00' * 88200))  # Simple empty sound
        
        # Get the current target (might be updated after reaching the previous one)
        if current_target_index < len(path_points):
            current_target = path_points[current_target_index]
            target_angle = calculate_angle(robot_pos, current_target)
            angle_error = (target_angle - robot_angle) % 360
            if angle_error > 180:
                angle_error -= 360
            distance = calculate_distance(robot_pos, current_target)
            
            # Draw line to current target
            pygame.draw.line(screen, YELLOW, robot_pos, current_target, 2)
            
            # Draw target direction arrow
            target_arrow_length = 40
            target_arrow_x = robot_pos[0] + target_arrow_length * math.cos(math.radians(target_angle))
            target_arrow_y = robot_pos[1] + target_arrow_length * math.sin(math.radians(target_angle))
            pygame.draw.line(screen, GREEN, robot_pos, (target_arrow_x, target_arrow_y), 2)
        elif len(path_points) > 0:
            # All targets reached - indicate this
            completed_text = font.render("Path Completed!", True, GREEN)
            screen.blit(completed_text, (FRAME_WIDTH // 2 - 60, 10))
    
    # Draw path lines
    if len(path_points) > 1:
        # Draw completed path segments in a different color
        if current_target_index > 0 and current_target_index <= len(path_points):
            # Draw completed segments
            pygame.draw.lines(screen, GREEN, False, path_points[:current_target_index], 3)
        
        # Draw remaining path segments
        if current_target_index < len(path_points) - 1:
            pygame.draw.lines(screen, BLUE, False, path_points[current_target_index:], 3)
    
    # Draw path points with different colors based on status
    for i, point in enumerate(path_points):
        if i < current_target_index:
            # Passed points
            pygame.draw.circle(screen, GREEN, point, 6)
        elif i == current_target_index:
            # Current target
            pygame.draw.circle(screen, PURPLE, point, 8)
        else:
            # Future targets
            pygame.draw.circle(screen, BLUE, point, 6)
    
    # Draw robot
    if marker_detected:
        # Draw robot
        pygame.draw.circle(screen, RED, (int(robot_pos[0]), int(robot_pos[1])), 15)
        
        # Draw direction indicator
        arrow_length = 25
        arrow_x = robot_pos[0] + arrow_length * math.cos(math.radians(robot_angle))
        arrow_y = robot_pos[1] + arrow_length * math.sin(math.radians(robot_angle))
        pygame.draw.line(screen, BLACK, (int(robot_pos[0]), int(robot_pos[1])), (int(arrow_x), int(arrow_y)), 3)
        pygame.draw.circle(screen, BLACK, (int(arrow_x), int(arrow_y)), 5)
        
        # Display essential information
        screen.blit(font.render("Marker Detected", True, (0, 100, 0)), (10, 10))
        
        if path_points and current_target_index < len(path_points):
            # Display key metrics
            aligned = abs(angle_error) < 10
            error_color = GREEN if aligned else RED
            screen.blit(font.render(f"Target: {current_target_index + 1}/{len(path_points)}", True, BLUE), (10, 40))
            screen.blit(font.render(f"Angle Error: {angle_error:.1f}°", True, error_color), (10, 70))
            screen.blit(font.render(f"Distance: {distance:.1f} px", True, BLUE), (10, 100))
            screen.blit(font.render(f"Status: {'Aligned' if aligned else 'Not aligned'}", True, error_color), (10, 130))
    else:
        # Draw inactive robot
        pygame.draw.circle(screen, (200, 200, 200), (int(robot_pos[0]), int(robot_pos[1])), 15)
        screen.blit(font.render("No Marker Detected", True, (200, 0, 0)), (10, 10))
    
    # Display instructions
    instr_text = font.render("Left-click: Add waypoint | C: Clear path | Q: Quit", True, (100, 100, 100))
    screen.blit(instr_text, (10, FRAME_HEIGHT - 30))
    
    # Show threshold setting
    threshold_text = font.render(f"Target reached threshold: {TARGET_REACHED_DISTANCE} px", True, (100, 100, 100))
    screen.blit(threshold_text, (10, FRAME_HEIGHT - 60))
    
    # Update display and cap the frame rate
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
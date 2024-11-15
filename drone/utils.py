import tellopy
import time

def send_drone_command(coordinates):
    """
    Send commands to the drone to fly to a specific location and spray.
    """
    try:
        # Connect to the drone
        drone = tellopy.Tello()
        drone.connect()
        drone.wait_for_connection(60.0)

        # Take off
        drone.takeoff()
        print("Drone taking off...")

        # Simulate flying to the given coordinates
        # This is an example, modify it to use GPS if supported by your drone
        drone.forward(50)  # Move forward 50 units
        time.sleep(5)  # Adjust sleep time based on how far you need to go

        # Simulate spraying action (customize if the drone supports spraying)
        print("Spraying...")
        drone.flip_forward()  # Fun flip as a placeholder for spray action
        time.sleep(2)

        # Land the drone
        drone.land()
        print("Drone landing...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        drone.quit()
        drone.close()

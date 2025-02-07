import threading
import time

# Task 1: Count numbers
def count_numbers():
    for i in range(1, 11):
        print(f"Count: {i}")
        time.sleep(1)  # Sleep for 1 second to simulate work

# Task 2: Print messages
def print_message(stop_event):
    while not stop_event.is_set():
        print("Hello, World!")
        time.sleep(1)  # Sleep for 1 second to simulate work

# Main function to start both threads
def main():
    # Create an event to stop the print_message thread
    stop_event = threading.Event()

    # Create two threads
    thread1 = threading.Thread(target=count_numbers)
    thread2 = threading.Thread(target=print_message, args=(stop_event,))

    # Start both threads
    print("Starting threads...")
    thread1.start()
    thread2.start()

    # Wait for the counting thread to finish
    thread1.join()

    # The message printing thread is infinite, so we'll let it run for a while
    time.sleep(5)  # Let the print_message thread run for 5 seconds
    print("Ending program...")

    # Signal the print_message thread to stop
    stop_event.set()
    thread2.join()

if __name__ == "__main__":
    main()

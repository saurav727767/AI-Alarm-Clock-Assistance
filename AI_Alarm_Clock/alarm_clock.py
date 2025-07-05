import time
from datetime import datetime
import threading
import pygame

# ---- Global flag to stop alarm ----
stop_flag = False

# ---- Function to validate time format ----
def is_valid_time(alarm_str):
    try:
        time.strptime(alarm_str, "%H:%M")
        return True
    except ValueError:
        return False

# ---- Function to listen for stop command ----
def listen_for_stop():
    global stop_flag
    while True:
        user_input = input()
        if user_input.strip().lower() == "stop":
            stop_flag = True
            break

# ---- Function to play looping sound ----
def play_looping_alarm():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("alarm.mp3")  # ensure the file exists
    pygame.mixer.music.play(loops=-1)  # 🔁 Play on infinite loop

# ---- Alarm ring and snooze logic ----
def ring_alarm():
    global stop_flag

    print("🔕 Type 'stop' and press Enter to stop the alarm.")

    # Start thread to listen for 'stop'
    stop_thread = threading.Thread(target=listen_for_stop)
    stop_thread.daemon = True
    stop_thread.start()

    while not stop_flag:
        print("🔔 Alarm Ringing (Looping sound)...")

        play_looping_alarm()  # 🔁 start playing on loop

        # Let it ring for 30 seconds or until stopped
        for _ in range(30):
            if stop_flag:
                pygame.mixer.music.stop()
                print("⏹️ Alarm stopped by user.")
                return
            time.sleep(1)

        pygame.mixer.music.stop()

        if not stop_flag:
            print("⏰ Snoozing for 1 minutes...\n")
            for _ in range(60):
                if stop_flag:
                    print("⏹️ Alarm stopped by user during snooze.")
                    return
                time.sleep(1)

# ---- Main alarm function ----
def alarm_clock():
    global stop_flag
    print("⏰ Welcome to AI Alarm Clock Assistant ⏰")
    alarm_time = input("🔹 Enter alarm time in HH:MM format (24-hour): ")

    if not is_valid_time(alarm_time):
        print("❌ Invalid time format! Use HH:MM like 06:30 or 18:45")
        return

    print(f"✅ Alarm set for {alarm_time}. Waiting...")

    while True:
        current_time = datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            print(f"\n⏰ WAKE UP! IT'S {current_time} ⏰")
            ring_alarm()
            break
        time.sleep(10)

# ---- Run the program ----
if __name__ == "__main__":
    alarm_clock()

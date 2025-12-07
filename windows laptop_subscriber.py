#windows laptop_subscriber.py
import paho.mqtt.client as mqtt
import time
from filters import moving_average
from fft_processing import add_sample, compute_fft 
from spotify_control import play_pause_toggle, skip_track
# Thresholds for clap detection
TAP_THRESHOLD = 700
DOUBLE_TAP_WINDOW = 1  # seconds
last_clap_time = 0.0
prev_filtered = 0.0
def on_message(client, userdata, msg):
    global last_clap_time

    try:
        raw_val = int(msg.payload.decode())
    except ValueError:
        print("Invalid payload received:", msg.payload)
        return

    # Basic logging
    print("Received:", raw_val)

    # 1. Filter
    #filtered = moving_average(raw_val)
    filtered = raw_val
    # 2. Add to FFT buffer
    add_sample(raw_val)

    # 3. Compute FFT
    fft_mag = compute_fft()
    if fft_mag is not None:
        energy = fft_mag.sum()
        print(f"Raw={raw_val}, Filtered={filtered:.2f}, FFT Energy={energy:.2f}")
    else:
        print(f"Raw={raw_val}, Filtered={filtered:.2f}")

    # 4. Clap detection
    is_rising = prev_filtered <= TAP_THRESHOLD and filtered > TAP_THRESHOLD

    if is_rising and (now - last_clap_time) > 0.2:
        dt = now - last_clap_time
        if 0 < (now - last_clap_time) < DOUBLE_TAP_WINDOW:
            print("DOUBLE TAP → skip track")
            skip_track()
        else:
            print("SINGLE TAP → toggle play/pause")
            play_pause_toggle()

        last_clap_time = now


client = mqtt.Client()
client.on_message = on_message

client.connect("172.20.10.7", 1883, 60)
client.subscribe("project/raw_sound")

client.loop_forever()
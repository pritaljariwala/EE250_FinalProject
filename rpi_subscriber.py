# laptop_subscriber.py
import paho.mqtt.client as mqtt
from filters import moving_average
from fft_processing import add_sample, compute_fft 

def on_message(client, userdata, msg):
    raw_value = int(msg.payload.decode())
    print("Received:", raw_value)

    try:
        raw_val = int(msg.payload.decode())

        # 1. Filter
        filtered = moving_average(raw_val)

        # 2. Add to FFT buffer
        add_sample(filtered)

        # 3. Compute FFT when ready
        fft_mag = compute_fft()
        if fft_mag is not None:
            energy = fft_mag.sum()
            print(f"Raw={raw_val}, Filtered={filtered:.2f}, FFT Energy={energy:.2f}")
        else:
            print(f"Raw={raw_val}, Filtered={filtered:.2f}")

    except ValueError:
        print("Invalid payload received.")

client = mqtt.Client()
client.on_message = on_message

client.connect("172.20.10.6", 1883, 60)
client.subscribe("project/raw_sound")

client.loop_forever()

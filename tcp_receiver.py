import socket

# TCP Configuration
TCP_HOST = "172.20.10.7"  
TCP_PORT = 65432          

def start_tcp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((TCP_HOST, TCP_PORT))
            print(f"Connected to TCP server at {TCP_HOST}:{TCP_PORT}")

            while True:
                data = client_socket.recv(1024) 
                if not data:
                    break  # No more data, exit the loop
                
                # Decode
                decoded_data = data.decode('utf-8')
                print(f"Received from server: {decoded_data}")

                process_data(decoded_data)
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("Connection closed.")
            client_socket.close()

def process_data(data):
    print(f"Processing data: {data}")

if __name__ == "__main__":
    start_tcp_client()

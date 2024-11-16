#!/usr/bin/env python3

import multiprocessing
import socket
import time
import subprocess

import os
import sys

# Change process name
def set_process_name(name: str):
    """Set the current process name."""
    # Change `sys.argv[0]` for tools like `ps`
    sys.argv[0] = name

    # Write to `/proc/self/comm` for tools like `htop`
    try:
        with open("/proc/self/comm", "w") as comm_file:
            comm_file.write(name)
    except FileNotFoundError:
        print("Error: Unable to change process name. /proc/self/comm not found.")
    except PermissionError:
        print("Error: Insufficient permissions to change process name.")

def sender_process(host: str, port: int):
    time.sleep(.5)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        for i in range(10):  # Send 10 packets
            message = f"Packet {i + 1}"
            sock.sendall(message.encode())
            print(f"Sender: Sent {message}")
            time.sleep(0.1)  # 100ms delay
    print("Sender: Finished sending packets")


def receiver_process(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((host, port))
        server_sock.listen(1)
        conn, addr = server_sock.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break


def perf_recorder_process():
    cmd = "perf record -a -e sched:sched_wakeup --filter comm=='xxx' -e sched:sched_switch --filter prev_comm=='xxx'||next_comm=='xxx' -- sleep 2"
    try:
        print("Perf Recorder: Starting perf recording...")
        subprocess.run(
                cmd.split(),
            check=True
        )
        print("Perf Recorder: Finished recording. Processing script output...")
        result = subprocess.run(
            ["perf", "script"],
            capture_output=True,
            text=True
        )
        print("Perf Recorder Output:")
        print("\n".join(result.stdout.splitlines()))
    except subprocess.CalledProcessError as e:
        print(f"Perf Recorder: Error occurred: {e}")
    except FileNotFoundError:
        print("Perf Recorder: 'perf' command not found. Please ensure it is installed.")
    print("Perf Recorder: Finished")


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345

    set_process_name("xxx")

    sender = multiprocessing.Process(target=sender_process, args=(HOST, PORT))
    receiver = multiprocessing.Process(target=receiver_process, args=(HOST, PORT))
    perf_recorder = multiprocessing.Process(target=perf_recorder_process)

    sender.start()
    receiver.start()
    perf_recorder.start()

    sender.join()
    receiver.join()
    perf_recorder.join()

    print("Application: All processes completed. Exiting.")


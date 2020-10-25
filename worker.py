import socket

# HOST = "ec2-3-86-27-100.compute-1.amazonaws.com"
HOST = "127.0.0.1"
PORT = 8888

HEADERSIZE = 99

def recv_word_counter(s):
    full_data = ''
    new_data = True
    while True:
        data = s.recv(4096)
        # print(data)
        if new_data:
            # print("new msg len:",data[:HEADERSIZE])
            data_len = int(data[:HEADERSIZE])
            # print(data_len)
            new_data = False

        # print(f"full message length: {data_len}")

        full_data += data.decode("utf-8")

        # print(len(full_data))

        if len(full_data)-HEADERSIZE == data_len:
            new_data = True
            # print(full_data[HEADERSIZE:])
            break

    return full_data

def word_counter(text):
    counts = dict()
    word_count = 0
    words = text.split()

    for word in words:
        word_count += 1
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return "[WORD COUNTER]\ntotal words: " + str(word_count) + " \n " + str(counts) + "\n[WORD COUNTER IS FINISHED]\n"

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM,) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(60)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)

            msg = "Word counter is running..."
            msg = f"{len(msg):<{HEADERSIZE}}"+msg
            conn.send(bytes(msg,"utf-8"))
            print('Word counter is running...')

            data = recv_word_counter(conn)
            count = word_counter(data[HEADERSIZE:])
            msg = f"{len(count):<{HEADERSIZE}}"+count
            conn.send(bytes(msg,"utf-8"))
            print('Word counter is finished.')
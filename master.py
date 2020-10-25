import socket, time

# HOST = "ec2-3-86-27-100.compute-1.amazonaws.com"
HOST = "127.0.0.1"
PORT = 8888

HEADERSIZE = 99

files = []
numf = input("Jumlah file: ")
print("Nama File(s):")
for i in range(int(numf)):
    files.append(input())

def recv_word_counter(s):
    full_data = ''
    new_data = True
    while True:
        data = s.recv(4096)
        if new_data:
            # print("new msg len:",data[:HEADERSIZE])
            data_len = int(data[:HEADERSIZE])
            new_data = False

        # print(f"full message length: {data_len}")

        full_data += data.decode("utf-8")

        # print(len(full_data))

        if len(full_data)-HEADERSIZE == data_len:
            new_data = True
            print(full_data[HEADERSIZE:])
            break

    return full_data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # f = open("data_large.txt", "r")
    # l = f.read()
    # f1 = open("data_small.txt", "r")
    # l1 = f1.read()
    # l_len = str(len(l)).encode()
    full = ""
    for f in files:
        txt = open(f,"r")
        r = txt.read()
        full += r

    msg = f"{len(full):<{HEADERSIZE}}"+ full
    s.send(bytes(msg,"utf-8"))

    print("-----")
    recv_word_counter(s) # print running state
    recv_word_counter(s) # print result / finished state

s.close()
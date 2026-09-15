import struct
from pyro_message import MAGIC, HEADER_FORMAT

def recv_message(sock,n):
    data = b''
    while len(data) < n:
        chunk = sock.recv(n-len(data))
        if not chunk:
            raise ConnectionError("Socket connection closed unexpectedly")
        data += chunk
    return data

def recieve_message(sock):
    header = recv_exact(sock, 40)
    
    (magic, version, msg_type, serializer, flags, seq,
     data_length, annotations_len, correlation_id,
     _, _) = struct.unpack(HEADER_FORMAT, header)
    
    if magic != MAGIC:
        raise ValueError(f"bad magic bytes: {magic!r}")
    
    if annotations_len != 0:
        raise NotImplementedError("Annotations chunks present are not handled, check your capture")
    
    payload =recv_exact(sock, data_length)
    
    return payload
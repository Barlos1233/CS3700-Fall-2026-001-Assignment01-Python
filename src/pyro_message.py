import struct
import serpent 

MAGIC = b'PYRO'
VERSION = 502    # Pyro5 protocal version 
MSG_CONNECT = 1
MSG_INVOKE = 4    
SERIALIZER_SERPENT = 1      # serializer id for serpent

HEADER_FORMAT = '>4sHBBHHII16sHH' # magic, version, flags, serializer id
# size I = 4 more bytes 

def build_header(msg_type, data_length, flags=0, seq=0, serializer=SERIALIZER_SERPENT, annotations_len=0, correlation_id=b'\x00'*16):
    header = struct.pack(
        HEADER_FORMAT,
        MAGIC, VERSION, msg_type, serializer,
        flags, seq, data_length, annotations_len, correlation_id,
        0, 0x4dc5
    )
    assert len(header) == 40
    return header

def build_list_request(prefix=""):
    
   # build the serpent-serialized payload
   
    call = ("Pyro.NameServer", "list_prefix", (prefix,), {})
    payload = serpent.dumps(call)
   
   # wrap it with size of length of the payload
    header = build_header(msg_type=MSG_INVOKE, data_length=len(payload))
   
   # concatenate header and payload
    return header + payload

def send_message(sock, msg):
    
    sock.sendall(msg)
def xrot(data: bytes, key: int = 0x42) -> bytes:
    # rotate-right 1 bit then XOR with key
    return bytes(((b >> 1 | (b << 7 & 0xFF)) ^ key) for b in data)

# test
if __name__ == "__main__":
    msg = b"hello"
    enc = xrot(msg)
    assert xrot(enc) == msg


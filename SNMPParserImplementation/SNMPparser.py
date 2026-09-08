
def read_tlv(data, offset):
    # Read tag
    tag = data[offset]
    offset += 1

    # Read length
    first = data[offset]
    offset += 1

    if first < 0x80:
        length = first
    else:
        n = first & 0x7F
        length = int.from_bytes(data[offset:offset+n], "big")
        offset += n

    # Read value
    value = data[offset:offset + length]
    offset += length

    return tag, value, offset


def parse_snmp(packet):

    # Outer SEQUENCE
    tag, message, _ = read_tlv(packet, 0)

    # Version
    tag, version_bytes, offset = read_tlv(message, 0)
    version = int.from_bytes(version_bytes, "big")

    # Community
    tag, community_bytes, offset = read_tlv(message, offset)
    community = community_bytes.decode("ascii")

    return version, community


packet = bytes.fromhex("""
30 26
02 01 01
04 06 70 75 62 6C 69 63
A0 19
02 01 01
02 01 00
02 01 00
30 0E
30 0C
06 08 2B 06 01 02 01 01 05 00
05 00
""")

version, community = parse_snmp(packet)

print("SNMP Version:", version)
print("Community:", community)

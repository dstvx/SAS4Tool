# Credits to https://gitlab.com/an-sasza4-projects/sasza4-py-kucingoren

from typing import SupportsInt, BinaryIO, Iterator, Union
from io import DEFAULT_BUFFER_SIZE, FileIO
from pathlib import Path
from numpy import array as nparray, uint32, uint8
from functools import lru_cache

HEADER_SIZE: int = 14
HEADER_MAGIC: bytes = b"DGDATA"
CHECKSUM_SIZE: int = HEADER_SIZE - len(HEADER_MAGIC)

BYTEHASH_TABLE = nparray((
    0x00000000, 0x09073096, 0x120E612C, 0x1B0951BA, 0xFF6DC419,
    0xF66AF48F, 0xED63A535, 0xE46495A3, 0xFEDB8832, 0xF7DCB8A4,
    0xECD5E91E, 0xE5D2D988, 0x01B64C2B, 0x08B17CBD, 0x13B82D07,
    0x1ABF1D91, 0xFDB71064, 0xF4B020F2, 0xEFB97148, 0xE6BE41DE,
    0x02DAD47D, 0x0BDDE4EB, 0x10D4B551, 0x19D385C7, 0x036C9856,
    0x0A6BA8C0, 0x1162F97A, 0x1865C9EC, 0xFC015C4F, 0xF5066CD9,
    0xEE0F3D63, 0xE7080DF5, 0xFB6E20C8, 0xF269105E, 0xE96041E4,
    0xE0677172, 0x0403E4D1, 0x0D04D447, 0x160D85FD, 0x1F0AB56B,
    0x05B5A8FA, 0x0CB2986C, 0x17BBC9D6, 0x1EBCF940, 0xFAD86CE3,
    0xF3DF5C75, 0xE8D60DCF, 0xE1D13D59, 0x06D930AC, 0x0FDE003A,
    0x14D75180, 0x1DD06116, 0xF9B4F4B5, 0xF0B3C423, 0xEBBA9599,
    0xE2BDA50F, 0xF802B89E, 0xF1058808, 0xEA0CD9B2, 0xE30BE924,
    0x076F7C87, 0x0E684C11, 0x15611DAB, 0x1C662D3D, 0xF6DC4190,
    0xFFDB7106, 0xE4D220BC, 0xEDD5102A, 0x09B18589, 0x00B6B51F,
    0x1BBFE4A5, 0x12B8D433, 0x0807C9A2, 0x0100F934, 0x1A09A88E,
    0x130E9818, 0xF76A0DBB, 0xFE6D3D2D, 0xE5646C97, 0xEC635C01,
    0x0B6B51F4, 0x026C6162, 0x196530D8, 0x1062004E, 0xF40695ED,
    0xFD01A57B, 0xE608F4C1, 0xEF0FC457, 0xF5B0D9C6, 0xFCB7E950,
    0xE7BEB8EA, 0xEEB9887C, 0x0ADD1DDF, 0x03DA2D49, 0x18D37CF3,
    0x11D44C65, 0x0DB26158, 0x04B551CE, 0x1FBC0074, 0x16BB30E2,
    0xF2DFA541, 0xFBD895D7, 0xE0D1C46D, 0xE9D6F4FB, 0xF369E96A,
    0xFA6ED9FC, 0xE1678846, 0xE860B8D0, 0x0C042D73, 0x05031DE5,
    0x1E0A4C5F, 0x170D7CC9, 0xF005713C, 0xF90241AA, 0xE20B1010,
    0xEB0C2086, 0x0F68B525, 0x066F85B3, 0x1D66D409, 0x1461E49F,
    0x0EDEF90E, 0x07D9C998, 0x1CD09822, 0x15D7A8B4, 0xF1B33D17,
    0xF8B40D81, 0xE3BD5C3B, 0xEABA6CAD, 0xEDB88320, 0xE4BFB3B6,
    0xFFB6E20C, 0xF6B1D29A, 0x12D54739, 0x1BD277AF, 0x00DB2615,
    0x09DC1683, 0x13630B12, 0x1A643B84, 0x016D6A3E, 0x086A5AA8,
    0xEC0ECF0B, 0xE509FF9D, 0xFE00AE27, 0xF7079EB1, 0x100F9344,
    0x1908A3D2, 0x0201F268, 0x0B06C2FE, 0xEF62575D, 0xE66567CB,
    0xFD6C3671, 0xF46B06E7, 0xEED41B76, 0xE7D32BE0, 0xFCDA7A5A,
    0xF5DD4ACC, 0x11B9DF6F, 0x18BEEFF9, 0x03B7BE43, 0x0AB08ED5,
    0x16D6A3E8, 0x1FD1937E, 0x04D8C2C4, 0x0DDFF252, 0xE9BB67F1,
    0xE0BC5767, 0xFBB506DD, 0xF2B2364B, 0xE80D2BDA, 0xE10A1B4C,
    0xFA034AF6, 0xF3047A60, 0x1760EFC3, 0x1E67DF55, 0x056E8EEF,
    0x0C69BE79, 0xEB61B38C, 0xE266831A, 0xF96FD2A0, 0xF068E236,
    0x140C7795, 0x1D0B4703, 0x060216B9, 0x0F05262F, 0x15BA3BBE,
    0x1CBD0B28, 0x07B45A92, 0x0EB36A04, 0xEAD7FFA7, 0xE3D0CF31,
    0xF8D99E8B, 0xF1DEAE1D, 0x1B64C2B0, 0x1263F226, 0x096AA39C,
    0x006D930A, 0xE40906A9, 0xED0E363F, 0xF6076785, 0xFF005713,
    0xE5BF4A82, 0xECB87A14, 0xF7B12BAE, 0xFEB61B38, 0x1AD28E9B,
    0x13D5BE0D, 0x08DCEFB7, 0x01DBDF21, 0xE6D3D2D4, 0xEFD4E242,
    0xF4DDB3F8, 0xFDDA836E, 0x19BE16CD, 0x10B9265B, 0x0BB077E1,
    0x02B74777, 0x18085AE6, 0x110F6A70, 0x0A063BCA, 0x03010B5C,
    0xE7659EFF, 0xEE62AE69, 0xF56BFFD3, 0xFC6CCF45, 0xE00AE278,
    0xE90DD2EE, 0xF2048354, 0xFB03B3C2, 0x1F672661, 0x166016F7,
    0x0D69474D, 0x046E77DB, 0x1ED16A4A, 0x17D65ADC, 0x0CDF0B66,
    0x05D83BF0, 0xE1BCAE53, 0xE8BB9EC5, 0xF3B2CF7F, 0xFAB5FFE9,
    0x1DBDF21C, 0x14BAC28A, 0x0FB39330, 0x06B4A3A6, 0xE2D03605,
    0xEBD70693, 0xF0DE5729, 0xF9D967BF, 0xE3667A2E, 0xEA614AB8,
    0xF1681B02, 0xF86F2B94, 0x1C0BBE37, 0x150C8EA1, 0x0E05DF1B,
    0x0702EF8D), uint32)


class DGDataDecodeError(Exception):
    """Failed to decode."""


class DGDataHash:
    def __init__(self, data: bytes | None = None) -> None:
        self.DIGEST = uint32(0)
        if data:
            self.update(data)

    def update(self, data: bytes) -> None:
        loc7 = self.DIGEST
        for teh_byte in iter(data):
            loc2 = teh_byte
            loc3 = (loc7 ^ loc2) & 255
            loc7 = ((loc7 >> 8) & 16777215) ^ BYTEHASH_TABLE[loc3]
        self.DIGEST = uint32(loc7)

    def digest(self) -> bytes:
        return self.hexdigest().encode('ascii')

    def hexdigest(self) -> str:
        return formatChecksumHex(self.DIGEST)

class Encoder:
    def __init__(self, size: int | None = None) -> None:
        self.hash = DGDataHash()
        self.data_cursor: int = 0
        self.data_size: int = -1 if size is None else size

    @property
    def hexchecksum(self) -> str:
        return self.hash.hexdigest()

    def digest(self, data: bytes) -> bytes:
        new_cursor = self.data_cursor + len(data)
        total_size = self.data_size
        if total_size > -1 and new_cursor > total_size:
            raise ValueError("Data cursor is exceeded the data size")
        retval = bytes(encodeByte(v, i) for i, v in enumerate(iter(data), self.data_cursor))
        self.hash.update(data)
        self.data_cursor = new_cursor
        return retval

class Decoder:
    def __init__(self, size: int | None = None, checksum: bytes | int | str | None = None) -> None:
        self.hash = DGDataHash()
        self.data_cursor: int = 0
        self.data_size: int = -1 if size is None else size
        self.dataChecksum = checksum

    def digest(self, data: bytes) -> bytes:
        new_cursor = self.data_cursor + len(data)
        total_size = self.data_size
        if total_size > -1 and new_cursor > total_size:
            raise ValueError("Data cursor is exceeded the data size")
        retval = bytes(decodeByte(v, i) for i, v in enumerate(iter(data), self.data_cursor))
        self.hash.update(retval)
        self.data_cursor = new_cursor
        return retval

def formatChecksumHex(checksum: SupportsInt) -> str:
    return f'{checksum:0{CHECKSUM_SIZE:d}x}'

def getChecksum(data: bytes) -> bytes:
    retval: bytes = data[:HEADER_SIZE]
    if not retval.startswith(HEADER_MAGIC):
        raise ValueError("Header is not found")
    return retval[len(HEADER_MAGIC):]

@lru_cache(maxsize=512)
def encodeByte(v: int, cursor: int = 0) -> int:
    v += cursor % 6
    v += 21
    return int(uint8(v))

@lru_cache(maxsize=512)
def decodeByte(v: int, cursor: int = 0) -> int:
    v -= 21
    v -= cursor % 6
    return int(uint8(v))


def iterDecodeFromFile(file: Union[BinaryIO, Path, str], data_size: int | None = None, buffer_size: int = DEFAULT_BUFFER_SIZE, verify: bool = False) -> Iterator[bytes]:
    try:
        if isinstance(file, (str, Path)):
            fp = FileIO(file, "rb")
        else:
            fp = file

        try:
            data_size = fp.seek(0, 2) if data_size is None else data_size
            fp.seek(0)
            dataChecksum = None
            buf = fp.read(HEADER_SIZE)
            try:
                dataChecksum = getChecksum(buf)
            except ValueError:
                if verify:
                    raise
            else:
                if data_size is not None:
                    data_size -= HEADER_SIZE
                    if data_size < 0:
                        raise ValueError(f"Expected header bytes length to be {HEADER_SIZE}, got {HEADER_SIZE + data_size}")
            decoder = Decoder(data_size, dataChecksum)
            if not dataChecksum and buf:
                yield decoder.digest(buf)
            while chunk := fp.read(buffer_size):
                yield decoder.digest(chunk)
            if verify:
                if not decoder.hash.digest() == decoder.dataChecksum:
                    raise ValueError(f"Expected checksum to be {dataChecksum.decode('utf8')}, got {decoder.hash.hexdigest()}")
        finally:
            if isinstance(file, (str, Path)):
                fp.close()
    except BaseException as exc:
        raise DGDataDecodeError(exc)


def encodeToFile(buffer: Union[bytes, bytearray, memoryview, Path], fp: BinaryIO, buffer_size: int = DEFAULT_BUFFER_SIZE) -> None:
    if isinstance(buffer, Path):
        buffer = buffer.read_bytes()
    encoder = Encoder(len(buffer))
    fp.write(HEADER_MAGIC)
    fp.write(b'\x00' * CHECKSUM_SIZE)
    for i in range(0, len(buffer), buffer_size):
        chunk = buffer[i:i+buffer_size]
        fp.write(encoder.digest(chunk))
    fp.seek(-encoder.data_cursor - CHECKSUM_SIZE, 1)
    fp.write(encoder.hexchecksum.encode("ascii"))
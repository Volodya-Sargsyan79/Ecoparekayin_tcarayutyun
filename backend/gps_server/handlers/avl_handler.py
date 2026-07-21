from dataclasses import dataclass


@dataclass
class AVLPacketInfo:
    codec_id: int
    codec_name: str
    record_count: int
    data_length: int
    raw_packet: bytes


class AVLHandler:

    CODEC_NAMES = {
        0x08: "Codec8",
        0x8E: "Codec8 Extended",
    }

    @classmethod
    def inspect_packet(
        cls,
        data_length: int,
        avl_data: bytes,
        crc: bytes,
    ) -> AVLPacketInfo:
        if len(avl_data) != data_length:
            raise ValueError(
                f"Invalid AVL data length: expected={data_length}, "
                f"received={len(avl_data)}"
            )

        if len(avl_data) < 3:
            raise ValueError("AVL packet is too short")

        codec_id = avl_data[0]
        record_count_1 = avl_data[1]
        record_count_2 = avl_data[-1]

        if record_count_1 != record_count_2:
            raise ValueError(
                "Record count mismatch: "
                f"first={record_count_1}, second={record_count_2}"
            )

        codec_name = cls.CODEC_NAMES.get(
            codec_id,
            f"Unknown Codec 0x{codec_id:02X}",
        )

        raw_packet = (
            b"\x00\x00\x00\x00"
            + data_length.to_bytes(4, byteorder="big")
            + avl_data
            + crc
        )

        return AVLPacketInfo(
            codec_id=codec_id,
            codec_name=codec_name,
            record_count=record_count_1,
            data_length=data_length,
            raw_packet=raw_packet,
        )
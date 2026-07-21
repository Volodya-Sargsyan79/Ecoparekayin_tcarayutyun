import socket
import threading
import traceback

# Բեռնում է Django-ն մինչև մոդելների import-ը
import gps_server.settings  # noqa: F401

from gps_server.handlers.avl_handler import AVLHandler
from gps_server.handlers.imei_handler import IMEIHandler
from gps_server.utils.socket_utils import recv_exact


HOST = "0.0.0.0"
PORT = 5027


def handle_client(
    client: socket.socket,
    address: tuple[str, int],
) -> None:
    print(f"\nNew connection: {address}")

    try:
        client.settimeout(120)

        # -------------------------------------------------
        # 1. IMEI handshake
        # -------------------------------------------------

        imei_length_bytes = recv_exact(client, 2)
        imei_length = int.from_bytes(
            imei_length_bytes,
            byteorder="big",
        )

        if imei_length <= 0 or imei_length > 30:
            raise ValueError(
                f"Invalid IMEI length: {imei_length}"
            )

        imei_bytes = recv_exact(client, imei_length)
        imei = imei_bytes.decode("ascii")

        print(f"IMEI length: {imei_length}")
        print(f"IMEI: {imei}")

        if not IMEIHandler.authenticate(imei):
            print("Unknown or inactive device")

            # 00 նշանակում է՝ IMEI-ն մերժված է
            client.sendall(b"\x00")
            return

        print("Device Authorized")

        # 01 նշանակում է՝ IMEI-ն ընդունված է
        client.sendall(b"\x01")

        # -------------------------------------------------
        # 2. AVL տվյալների ընդունում
        # -------------------------------------------------

        while True:
            try:
                # Preamble՝ 4 բայթ
                preamble = recv_exact(client, 4)
            except ConnectionError:
                print(f"Device disconnected: {imei}")
                break

            if preamble != b"\x00\x00\x00\x00":
                raise ValueError(
                    f"Invalid preamble: {preamble.hex()}"
                )

            # Data Field Length՝ 4 բայթ
            data_length_bytes = recv_exact(client, 4)
            data_length = int.from_bytes(
                data_length_bytes,
                byteorder="big",
            )

            if data_length <= 0 or data_length > 1_000_000:
                raise ValueError(
                    f"Invalid data length: {data_length}"
                )

            # Codec ID-ից մինչև երկրորդ Record Count-ը
            avl_data = recv_exact(client, data_length)

            # CRC՝ 4 բայթ
            crc = recv_exact(client, 4)

            packet = AVLHandler.inspect_packet(
                data_length=data_length,
                avl_data=avl_data,
                crc=crc,
            )

            print("--------------------------------")
            print(f"IMEI: {imei}")
            print(f"Codec ID: 0x{packet.codec_id:02X}")
            print(f"Codec: {packet.codec_name}")
            print(f"Data length: {packet.data_length}")
            print(f"Records: {packet.record_count}")
            print(f"CRC received: {crc.hex()}")
            print(f"Full packet HEX: {packet.raw_packet.hex()}")
            print("--------------------------------")

            # Սարքին հայտնում ենք՝ քանի Record ենք ընդունել
            response = packet.record_count.to_bytes(
                4,
                byteorder="big",
            )

            client.sendall(response)

            print(
                "AVL acknowledgement sent:",
                response.hex(),
            )

    except socket.timeout:
        print(f"Connection timeout: {address}")

    except (ConnectionError, UnicodeDecodeError, ValueError) as error:
        print(f"Protocol error from {address}: {error}")

    except Exception:
        print(f"Unexpected error from {address}")
        traceback.print_exc()

    finally:
        client.close()
        print(f"Connection closed: {address}")


def start_server() -> None:
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1,
    )

    server.bind((HOST, PORT))
    server.listen(100)

    print(f"Listening on {HOST}:{PORT}")

    try:
        while True:
            client, address = server.accept()

            thread = threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True,
            )

            thread.start()

    except KeyboardInterrupt:
        print("\nStopping GPS server...")

    finally:
        server.close()


if __name__ == "__main__":
    start_server()
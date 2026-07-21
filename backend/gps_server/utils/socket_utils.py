import socket


def recv_exact(client: socket.socket, size: int) -> bytes:
    """
    TCP կապից ստանում է ճիշտ նշված քանակի բայթեր։

    client.recv(size)-ը պարտադիր չէ մեկ անգամով վերադարձնի
    բոլոր պահանջված բայթերը, դրա համար կարդում ենք ցիկլով։
    """
    data = bytearray()

    while len(data) < size:
        chunk = client.recv(size - len(data))

        if not chunk:
            raise ConnectionError(
                "Client disconnected before all data was received"
            )

        data.extend(chunk)

    return bytes(data)
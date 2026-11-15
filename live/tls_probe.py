from __future__ import annotations

import socket
import ssl


HOST = "birder.jinsiqie.life"
PORT = 443


def main() -> int:
    raw = socket.create_connection((HOST, PORT), timeout=15)
    context = ssl.create_default_context()
    tls = context.wrap_socket(raw, server_hostname=HOST)
    print("version:", tls.version())
    print("cipher:", tls.cipher())
    print("alpn:", tls.selected_alpn_protocol())
    try:
        tls.sendall(
            (
                f"GET /xb/iil HTTP/1.1\r\n"
                f"Host: {HOST}\r\n"
                "Connection: close\r\n"
                "\r\n"
            ).encode("ascii")
        )
        response = tls.recv(512)
        print("response_head:", response.split(b"\r\n", 1)[0].decode("latin1"))
    finally:
        tls.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

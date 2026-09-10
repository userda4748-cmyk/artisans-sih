from rembg import new_session, remove

_session = None


def get_session():
    global _session
    if _session is None:
        _session = new_session("u2net")
    return _session


def remove_background(image_bytes: bytes) -> bytes:
    session = get_session()
    result = remove(
        image_bytes,
        session=session,
        force_return_bytes=True,
    )

    if not isinstance(result, bytes):
        raise TypeError("rembg did not return bytes")

    return result
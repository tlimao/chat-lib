from freedomlib.utils.serializable import Serializable

MESSAGE: str = "I'm a 64º Ricky"
MESSAGE_BYTES: bytes = b"I'm a 64\xc2\xba Ricky"
MESSAGE_B64: str = "SSdtIGEgNjTCuiBSaWNreQ=="

def test_str_to_bytes() -> None:
    message: str = MESSAGE
    message_bytes: bytes = MESSAGE_BYTES

    message_result: bytes = Serializable.str_to_bytes(message)
    
    assert isinstance(message_result, bytes), "The result is not of type bytes."
    assert message_bytes == message_result, "The converted bytes do not match the expected value."


def test_b64_str_to_bytes() -> None:
    base64_message: str = MESSAGE_B64  # Represents the string "I'm a 64º" in base64
    expected_bytes: bytes = MESSAGE_BYTES  # Expected bytes

    result_bytes: bytes = Serializable.b64_str_to_bytes(base64_message)

    assert isinstance(result_bytes, bytes), "The result is not of type bytes."
    assert expected_bytes == result_bytes, "The decoded bytes do not match the expected value."


def test_bytes_to_str() -> None:
    message_bytes: bytes = MESSAGE_BYTES
    expected_message: str = MESSAGE

    result_message: str = Serializable.bytes_to_str(message_bytes)

    assert isinstance(result_message, str), "The result is not of type str."
    assert expected_message == result_message, "The converted string does not match the expected value."


def test_bytes_to_b64_str() -> None:
    message_bytes: bytes = MESSAGE_BYTES
    expected_b64_message: str = MESSAGE_B64  # Corresponding base64 string

    result_b64_message: str = Serializable.bytes_to_b64_str(message_bytes)
    
    assert isinstance(result_b64_message, str), "The result is not of type str."
    assert expected_b64_message == result_b64_message, "The converted base64 string does not match the expected value."

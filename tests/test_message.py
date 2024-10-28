import os
import json

from freedomlib.crypto.functions import ED25519, X25519
from freedomlib.key.key_box import KeyBox
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes, base
from freedomlib.key.key_box import KeyBox
from freedomlib.utils.serializable import Serializable
from freedomlib.message.message import Message

MESSAGE: str = "Sanchez is your surname Ricky?"

def test_crypto_message() -> None:
    # Ricky keys
    ricky_aci: str = "0192cf8a-4acc-750b-b127-e5f45d9381af"
    ricky_x25519_private_key, ricky_x25519_public_key = X25519.create_key_pair()
    ricky_ed25519_private_key, ricky_ed25519_public_key = ED25519.create_key_pair()
    ricky_kbox: KeyBox = KeyBox(
        id="ricky_key_box_id",
        aci=ricky_aci,
        x25519_pub_key=ricky_x25519_public_key,
        ed25519_pub_key=ricky_ed25519_public_key
    )

    # Morty keys
    morty_aci: str = "0192cf8a-4acc-7b43-a8e6-3d64269c4270"
    morty_x25519_private_key, morty_x25519_public_key = X25519.create_key_pair()
    morty_ed25519_private_key, morty_ed25519_public_key = ED25519.create_key_pair()
    morty_kbox: KeyBox = KeyBox(
        id="morty_key_box_id",
        aci=morty_aci,
        x25519_pub_key=morty_x25519_public_key,
        ed25519_pub_key=morty_ed25519_public_key
    )
    
    # Morty send a message to Ricky
    message: str = MESSAGE
    
    morty_shared_key = X25519.shared_key(morty_x25519_private_key, ricky_kbox.x25519_pub_key)
    morty_derived_key = X25519.derive_key(morty_shared_key)
    
    nonce: bytes = os.urandom(12)

    encryptor: base.AEADEncryptionContext = Cipher(
        algorithms.AES(morty_derived_key),
        modes.GCM(nonce)).encryptor()
    
    chiper_message: bytes = encryptor.update(Serializable.str_to_bytes(message)) + encryptor.finalize()
    
    tag: bytes = encryptor.tag
    
    message_obj: Message = Message(
        cipher_message=chiper_message,
        id="dummy-message-id",
        nonce=nonce,
        sender_aci=morty_aci,
        recipient_aci=ricky_aci,
        tag=tag,
    )
    
    message_dict: dict = message_obj.to_dict()
    
    message_obj_rebuild: Message = Message.from_dict(message_dict)
    
    ricky_shared_key = X25519.shared_key(ricky_x25519_private_key, morty_kbox.x25519_pub_key)
    ricky_derived_key = X25519.derive_key(ricky_shared_key)
    
    decryptor: base.AEADEncryptionContext = Cipher(
        algorithms.AES(ricky_derived_key),
        modes.GCM(message_obj_rebuild.nonce, message_obj_rebuild.tag)).decryptor()
    
    original_message: str = Serializable.bytes_to_str(
        decryptor.update(message_obj_rebuild.cipher_message) + decryptor.finalize()
    )
    
    assert message == original_message


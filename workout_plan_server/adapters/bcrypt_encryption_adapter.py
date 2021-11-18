import bcrypt

from workout_plan_server.services.ports.encryption_adapter import EncryptionAdapter


class BCryptEncryptionAdapter(EncryptionAdapter):
    def encrypt_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_encrypted_password(self, password: str, encrypted_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), encrypted_password.encode("utf-8"))

from passlib.hash import argon2


class PasswordHasher:
    """Handles password hashing and verification."""

    @staticmethod
    def hash(password: str) -> str:
        """
        Hash a password.
        :param password: takes a plain text password and hashes it
        :return: returns the hashed password string
        """
        return argon2.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a hashed password against the plain text.
        :param plain_password: takes a plain text password
        :param hashed_password: takes a hashed text password
        :return: verify the hashed password against the plain text and return True or False
        """
        return argon2.verify(plain_password, hashed_password)

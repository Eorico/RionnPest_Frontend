from .base import BaseApiService, IAuthService

class AuthApiService(BaseApiService, IAuthService):

    def login_service(self, username: str, password: str) -> tuple[bool, str]:
        try:
            response = self._session.post(
                f"{self._base_url}/auth/login",
                json={"username": username, "password": password},
                timeout=5,
            )
            if response.status_code == 200:
                token = response.json().get("access_token")
                if token:
                    self._session.headers.update(
                        {"Authorization": f"Bearer {token}"})
                return True, "Login Successful"
            return False, "Invalid Credentials"
        except Exception as e:
            return False, f"Server Error: {e}"

    def register_service(self, username: str, password: str,
                         email: str) -> tuple[bool, str]:
        try:
            response = self._session.post(
                f"{self._base_url}/auth/register",
                json={"username": username, "password": password, "email": email},
                timeout=5,
            )
            if response.status_code == 201:
                return True, "Registered successfully"
            return False, response.json().get("detail", response.text)
        except Exception as e:
            return False, str(e)

    def forgot_password_service(self, username: str) -> tuple[bool, str]:
        try:
            response = self._session.post(
                f"{self._base_url}/auth/forgot-password",
                json={"username": username},
                timeout=10,
            )
            if response.status_code == 200:
                return True, response.json().get("message", "Code sent")
            return False, response.json().get("detail", response.text)
        except Exception as e:
            return False, str(e)

    def reset_password_service(self, username: str, otp: str,
                               new_password: str) -> tuple[bool, str]:
        try:
            response = self._session.post(
                f"{self._base_url}/auth/reset-password",
                json={"username": username, "otp": otp,
                      "new_password": new_password},
                timeout=5,
            )
            if response.status_code == 200:
                return True, "Password reset successfully"
            return False, response.json().get("detail", response.text)
        except Exception as e:
            return False, str(e)

    def logout_service(self) -> None:
        self._session.headers.pop("Authorization", None)
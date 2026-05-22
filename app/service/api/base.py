from abc import ABC, abstractmethod

class BaseApiService(ABC):
    def __init__(self, base_url: str, session):
        self._base_url = base_url
        self._session = session
 
class IAuthService(ABC):
    @abstractmethod
    def login_service(self, username: str, password: str) -> tuple[bool, str]: ...
 
    @abstractmethod
    def register_service(self, username: str, password: str,
                         email: str) -> tuple[bool, str]: ...
 
    @abstractmethod
    def forgot_password_service(self, username: str) -> tuple[bool, str]: ...
 
    @abstractmethod
    def reset_password_service(self, username: str, otp: str,
                               new_password: str) -> tuple[bool, str]: ...
 
    @abstractmethod
    def logout_service(self) -> None: ...
 
 
class IInventoryService(ABC):
    @abstractmethod
    def get_active_inventory(self) -> list: ...
 
    @abstractmethod
    def add_inventory_record(self, data: dict) -> tuple[bool, str]: ...
 
    @abstractmethod
    def update_inventory_record(self, record_id: int,
                                data: dict) -> tuple[bool, str]: ...
 
 
class IRecycleBinService(ABC):
    @abstractmethod
    def get_recycle_bin(self) -> list: ...
 
    @abstractmethod
    def move_to_bin(self, record_id: int) -> tuple[bool, str]: ...
 
    @abstractmethod
    def restore_record(self, record_id: int) -> tuple[bool, str]: ...
 
    @abstractmethod
    def restore_all(self) -> tuple[bool, str]: ...
 
    @abstractmethod
    def permanent_delete(self, record_id: int) -> tuple[bool, str]: ...
 
 
class IDocumentService(ABC):
    @abstractmethod
    def upload_document(self, title: str, file_name: str,
                        file_data: bytes) -> tuple[bool, str]: ...
 
    @abstractmethod
    def get_documents(self) -> list: ...
 
    @abstractmethod
    def download_document(self, doc_id: int) -> bytes | None: ...
 
    @abstractmethod
    def delete_document(self, doc_id: int) -> tuple[bool, str]: ...
 
 
class IConnectionService(ABC):
    @abstractmethod
    def check_connection_service(self) -> bool: ...

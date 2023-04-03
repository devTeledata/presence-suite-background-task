class PayloadSession:
    service_id: int
    name: str
    email: str
    language: str
    session_type: str
    remote_ip: str

    def __init__(self, service_id: int, name: str, email: str, language: str, session_type: str, remote_ip: str) -> None:
        self.service_id = service_id
        self.name = name
        self.email = email
        self.language = language
        self.session_type = session_type
        self.remote_ip = remote_ip

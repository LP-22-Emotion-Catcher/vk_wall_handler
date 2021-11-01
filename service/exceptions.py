
class UnknownWallError(Exception):

    def __init__(self, link: str) -> None:
        self.link = link
        super().__init__(f'Unknown wall: {link}')

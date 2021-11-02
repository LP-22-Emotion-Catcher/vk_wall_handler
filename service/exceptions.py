
class UnknownWallError(Exception):

    def __init__(self, wall_id: str) -> None:
        self.wall_id = wall_id
        super().__init__(f'Unknown wall: {wall_id}')

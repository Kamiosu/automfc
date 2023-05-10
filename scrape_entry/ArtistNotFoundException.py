
class ArtistNotFoundException(Exception):
    def __init__(self, artist):
        self.artist = artist
        super().__init__(f"Artist '{artist}' not found")
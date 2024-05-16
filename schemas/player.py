class Player:
    def __init__(self):
        self.location = 1
        self.fuel = 100
        self.station_power = 100

    def move(self, new_loc):
        if new_loc != self.location:
            self.location = new_loc
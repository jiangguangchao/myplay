class CarPlay:
    def __init__(self,
                 play_id=None,
                 myplay=None,
                 car_id=None,
                 rc_id=None,
                 start_time=None,
                 end_time=None,
                 play_time=None,
                 total_energy=None,
                 used_energy=None,
                 status='0'):
        self.play_id = play_id
        self.myplay = myplay
        self.car_id = car_id
        self.rc_id = rc_id
        self.start_time = start_time
        self.end_time = end_time
        self.play_time = play_time
        self.total_energy = total_energy
        self.used_energy = used_energy
        self.status = status

    def __repr__(self):
        return f"CarPlay(play_id={self.play_id}, myplay={self.myplay}, car_id={self.car_id}, rc_id={self.rc_id}, start_time={self.start_time}, play_time={self.play_time}, total_energy={self.total_energy}, used_energy={self.used_energy}, status={self.status})"
def play_movie(data, mqtt, redis):
    rc_id = data.get('rc_id')
    car_id = data.get('car_id')
    play_id = data.get('play_id')
    movie_id = data.get('movie_id')
    print(f"开始播放{movie_id}")

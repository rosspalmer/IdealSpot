from datetime import datetime, timedelta

from ideal_spot import EvaluateSpots, Spot, WeatherTarget
from ideal_spot.targets import IdealWindTarget, IdealTempTarget, NewRainTarget

"""
In this example we are going sailing! We also have a handy,
dandy transporter to set off anywhere the world we choose.
We will go twice, once right now for eight hours and then
again twenty fours later at the same spot (guess the
transporter broke?!). 

For sailing we want about 10 m/s, a temperature of ~295K (22C),
and no precipitation. While temperature and rain are important
to consider, wind is much more critical.
"""

# Generate spots

spots = {
    Spot('San Diego', 32.67, -117.41),
    Spot('Vancouver', 49.29, -123.29),
    Spot('Montego Bay', 18.47, -77.93),
    Spot('Athens', 37.93, 23.71),
    Spot('Auckland', -36.84, 174.77),
    Spot('Tokyo', 35.59, 139.86)}

# Get date ranges based on current time
start_time_first_day = datetime.now()
end_time_first_day = start_time_first_day + timedelta(hours=8)
start_time_second_day = start_time_first_day + timedelta(days=1)
end_time_second_day = start_time_second_day + timedelta(hours=8)

# Construct WeatherTarget based on sailing needs
target = WeatherTarget('79094518408cb847574557c958eeec91')
target = IdealWindTarget(target, 'wind_day_one', start_time_first_day, end_time_first_day, 10.0)
target = IdealWindTarget(target, 'wind_day_two', start_time_second_day, end_time_second_day, 10.0)
target = IdealTempTarget(target, 'temp_day_one', start_time_first_day, end_time_first_day, 295.0)
target = IdealTempTarget(target, 'temp_day_two', start_time_second_day, end_time_second_day, 295.0)
target = NewRainTarget(target, 'rain_day_one', start_time_first_day, end_time_first_day)
target = NewRainTarget(target, 'rain_day_two', start_time_second_day, end_time_second_day)

# Generate score weight map based on preferences
score_weights = {'wind_day_one': 2.0, 'wind_day_two': 2.0, 'temp_day_one': 0.5, 'temp_day_two': 0.5,
                 'rain_day_one': -0.5, 'rain_day_two': -0.5}

spots = EvaluateSpots.score_spots(spots, target, score_weights)
score_report = EvaluateSpots.generate_score_report(spots)
score_report = score_report.sort_values('overall_score', ascending=False)

print(score_report[['name', 'overall_score']])
print(score_report[['name', 'wind_day_one', 'wind_day_two']])
print(score_report[['name', 'rain_day_one', 'temp_day_one', 'rain_day_two', 'temp_day_two']])

"""

Example Output:

          name  overall_score
2    San Diego       4.358843
3     Auckland       4.341185
1       Athens       4.272057
5  Montego Bay       4.125707
4    Vancouver       3.966885
0        Tokyo       3.960065

          name  wind_day_one  wind_day_two
2    San Diego      0.861500      0.822417
3     Auckland      0.821417      0.873917
1       Athens      0.785583      0.862583
5  Montego Bay      0.862750      0.848667
4    Vancouver      0.779250      0.792500
0        Tokyo      0.925917      0.826833

          name  rain_day_one  temp_day_one  rain_day_two  temp_day_two
2    San Diego        0.0000      0.996317        0.0000      0.985703
3     Auckland        0.0000      0.948833        0.0000      0.952203
1       Athens        0.0000      0.975483        0.0000      0.975963
5  Montego Bay        0.1312      0.963483        0.4000      0.973463
4    Vancouver        0.1875      0.968367        0.0938      0.959703
0        Tokyo        1.0000      0.982967        0.0688      0.994963

"""
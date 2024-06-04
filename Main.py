from temperature import Temp_Freezing, Temp_Cool, Temp_Warm, Temp_Hot
from weather import Weather_Sunny, Weather_PartiallyCloudy, Weather_Overcast
from speed import Speed_Fast, Speed_Slow
import matplotlib.pyplot as plt
import numpy as np

def fuzzy_min(a, b):
    return a if a < b else b

def fuzzy_rule(temperature, cover):
    sunny = Weather_Sunny(cover)
    warm = Temp_Warm(temperature)
    cloudy = Weather_PartiallyCloudy(cover)
    cool = Temp_Cool(temperature)

    R1_Fast = fuzzy_min(sunny, warm)
    R2_Slow = fuzzy_min(cloudy, cool)
    
    y1 = R1_Fast
    y2 = R2_Slow

    return sunny, warm, cool, cloudy, y1,y2

def get_speed(temp_warm, temp_cool, weather_sunny, weather_cloudy):
    slow_degree = fuzzy_min(temp_cool, weather_cloudy)
    fast_degree = fuzzy_min(temp_warm, weather_sunny)
    speeds = np.linspace(0, 110, 1000)
    slow_output = [min(Speed_Slow(speed), slow_degree) for speed in speeds]
    fast_output = [min(Speed_Fast(speed), fast_degree) for speed in speeds]
    
    numerator = np.sum(speeds * slow_output) + np.sum(speeds * fast_output)
    denominator = np.sum(slow_output) + np.sum(fast_output)
    
    if denominator == 0:
        return 0
    else:
        return numerator / denominator

if __name__ == "__main__":
    temperature = float(input("Enter temperature: "))
    cloud_cover = float(input("Enter cloud cover: "))

    sunny, warm, cool, cloudy, y1, y2 = fuzzy_rule(temperature, cloud_cover)

    print(f'Sunny {sunny:.2f} & Warm {warm:.2f}')
    print(f'Cloudy {cloudy:.2f} & Cool {cool:.2f}')
    print(f'Fast {y1:.2f} Slow {y2:.2f}')

    speed = get_speed(warm, cool, sunny, cloudy)
    print(f'Speed: {speed:.2f} mph')

    temps = np.linspace(0, 110, 500)
    cloud_covers = np.linspace(0, 100, 500)

    freezing_values = [Temp_Freezing(temp) for temp in temps]
    cool_values = [Temp_Cool(temp) for temp in temps]
    warm_values = [Temp_Warm(temp) for temp in temps]
    hot_values = [Temp_Hot(temp) for temp in temps]

    sunny_values = [Weather_Sunny(cover) for cover in cloud_covers]
    partially_cloudy_values = [Weather_PartiallyCloudy(cover) for cover in cloud_covers]
    overcast_values = [Weather_Overcast(cover) for cover in cloud_covers]

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(temps, freezing_values, label='Freezing')
    plt.plot(temps, cool_values, label='Cool')
    plt.plot(temps, warm_values, label='Warm')
    plt.plot(temps, hot_values, label='Hot')

    plt.scatter([temperature], [warm], color='red', label=f'Warm: {warm:.2f}')
    plt.scatter([temperature], [cool], color='blue', label=f'Cool: {cool:.2f}')

    plt.xlabel('Temperature (°F)')
    plt.ylabel('Membership Value')
    plt.title('Temperature Membership Functions')
    plt.xticks(np.arange(0, 115, 5))
    plt.yticks(np.arange(0, 1.1, 0.2))
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(cloud_covers, sunny_values, label='Sunny')
    plt.plot(cloud_covers, partially_cloudy_values, label='Partially Cloudy')
    plt.plot(cloud_covers, overcast_values, label='Overcast')

    plt.scatter([cloud_cover], [sunny], color='orange', label=f'Sunny: {sunny:.2f}')
    plt.scatter([cloud_cover], [cloudy], color='gray', label=f'Cloudy: {cloudy:.2f}')

    plt.xlabel('Cloud Cover (%)')
    plt.ylabel('Membership Value')
    plt.title('Weather Membership Functions')
    plt.xticks(np.arange(0, 105, 5))
    plt.yticks(np.arange(0, 1.1, 0.2))
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(6, 5))

    speed_slow_values = [Speed_Slow(x) for x in temps]
    speed_fast_values = [Speed_Fast(x) for x in temps]

    speed_membership_value = min(1, y1, y2)

    plt.plot(temps, speed_slow_values, label='Slow')
    plt.plot(temps, speed_fast_values, label='Fast')

    plt.scatter([speed], [speed_membership_value], color='green', label=f'Calculated Speed: {speed:.2f}')

    plt.annotate(f'COG: {speed:.2f} mph', xy=(speed, speed_membership_value), xytext=(speed + 5, speed_membership_value - 0.1),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))

    plt.axhline(y=y1, color='gray', linestyle='--', label=f'y: {y1:.2f}')
    plt.axhline(y=y2, color='gray', linestyle='--', label=f'y: {y2:.2f}')

    plt.xlabel('Speed (mph)')
    plt.ylabel('Membership Value')
    plt.title('Speed Membership Functions')
    plt.xticks(np.arange(0, 115, 5))
    plt.yticks(np.arange(0, 1.1, 0.2))
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


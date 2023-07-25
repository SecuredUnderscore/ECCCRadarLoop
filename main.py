import os
import requests
import imageio

radarCallsign = "CASAG"
frames = False  # False for unlimited, an int for specific
url = f"https://dd.weather.gc.ca/radar/PRECIPET/GIF/{radarCallsign}/"
frameSize = (580, 480)
images = []
gifs = []


def keep_items_at_end(input_list, num_items_to_keep):
    if num_items_to_keep >= len(input_list):
        return input_list  # Nothing to remove, return the original list

    return input_list[-num_items_to_keep:]


try:
    os.remove("./output_video.mp4")
except:
    pass

response = requests.get(url)
contents = response.content
contents = str(contents).split("K ")

for content in contents:
    while True:
        if content[-1] == "<":
            content = content[:len(content) - 1]
            break
        else:
            content = content[:len(content) - 1]

    content = content.split(">")
    content = content[2]

    if "RAIN.gif" in content and "COMP" not in content:
        gifs.append(content)
    else:
        pass

if frames != False:  # Check if I want to use all the frames I can get
    gifs = keep_items_at_end(gifs, frames)

for content in gifs:
    print("Getting GIF from: " + url + content)
    with open('./temp.gif', 'wb') as f:
        f.write(requests.get(url + content).content)

    gif_path = os.path.join("./temp.gif")
    images.append(imageio.v2.imread(gif_path))
    os.remove("./temp.gif")

imageio.mimsave("./output_video.mp4", images, fps=10)  # Put it all together and save

## Running
```commandline
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt-get install python3-tk

python main.py
```

# Coordinate Transform 
To run code, video should be downloaded from [here](https://disk.yandex.ru/d/cSsaqIltoaPn9g) and put in ```coordinate_transform/data```.<br> 
File is named "yantar-230722-02-det.mp4" <br>
Also file should be downloaded from same directory: "yantar-230722-02_track.csv" and placed in ```coordinate_transform/data```
<br><br>
Module coordinate_transform is busy with transformation of coordinates
for our objects of observation. It also is able to transform camera positions for simulation.

# Camera Control
cam_control module provides an interface for controlling
the camera angles.

# Instruct the camera
instruct module is responsible for providing adjustments
to the camera angle based on the solutions of DTSP.

# TSP
the tsp module provides algorithmic framework
for finding the shortest path on a graph.
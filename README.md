## Running
To run code, video should be downloaded from [here](https://disk.yandex.ru/d/cSsaqIltoaPn9g) and put in ```coordinate_transform/data```.<br> 
File is named "yantar-230722-02-det.mp4" <br>
Also file should be downloaded from same directory: "yantar-230722-02_track.csv" and placed in ```coordinate_transform/data```
<br><br>

```commandline
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt-get install python3-tk

python main.py
```

# Coordinate Transform
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

# Simulation
Simulation module is concerned with testing the hypotheses and analyzing the best strategies for solving a problem.

# Evaluation results for KNN Solver:
Statistics for time in ticks (frames), given that 1 second equate to 25 ticks.
- Stats: count    100.00000 (Number of experiments)
- mean     408.56000
- std       46.73919
- min      305.00000
- 25%      375.75000
- 50%      412.50000
- 75%      442.25000
- max      549.00000

## Current bugs: 
#### cam_control
- Cam pitch shaking (players are not tracked immediately)

## TODO:
- No camera physics (enertion, angle speed)
- No prediction of players
- Players are moving randomly
- Players can block view
- Measure metrics
- Make camera adapt to ones player position on the fly
- Detect when player's face is facing the right direction
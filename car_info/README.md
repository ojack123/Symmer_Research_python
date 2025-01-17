# Car Information
This folder contains a number of ```.txt``` files associated with different vehicles in the simulation. Here is a description of each of them.

**Note on car information format:**  The ```.txt``` files contain three rows of data. The top row represents time (seconds). The second and third rows represent velocity (m/s) and heading angle (rad) respectively, at the associated time. The initial positions of vehicles 1-3 can be found in ```car_info.xlsx```.

```car_0_full_knowledge.txt``` Contains the velocity and heading angle at each time step for the resulting path generated by the parthfinding algorithm given a "full knowledge" scenario of the highway. 

```car_0_partial_knowledge.txt``` Contains the velocity and heading angle at each time step for the resulting path generated by the parthfinding algorithm given a "partial knowledge" scenario of the highway. 

```car_0.txt``` Contains the most recent ego vehicle path generated by the pathfinding algorithm. If you wish to save the path you must rename this file to something else since it is overwritten after running the path planner.

```car_[1-3].txt``` These vehicles represent the "actors" and are identical to those from Evan's highway scenario.

```car_info.xlsx``` and ```code``` Are not used and may be ignored.

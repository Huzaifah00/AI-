# AI-
Dynamic Pathfinding Agent - README
Project Overview
This project implements an intelligent agent capable of navigating a grid-based environment using Informed Search Algorithms. It features real-time path re-planning to handle dynamic obstacles that appear while the agent is in motion.
Core Features
•	Dynamic Grid Sizing: Interactive grid with customizable wall placement.
•	Search Algorithms: Implementation of A* Search and Greedy Best-First Search (GBFS).
•	Heuristics: Toggle between Manhattan and Euclidean distance functions.
•	Dynamic Mode: Obstacles spawn randomly during transit, triggering immediate path re-planning.
•	Metrics Dashboard: Real-time tracking of Nodes Visited, Path Cost, and Execution Time.
Installation & Setup
Ensure you have Python installed on your system. You will need the Pygame library to run the GUI.
Install dependencies using pip:
pip install pygame
How to Run
Execute the main script from your terminal or command prompt:
python 23f0688_ai
Interface Controls
Key / Action	Function
Left Click	Place Wall
Right Click	Erase Wall
SPACE	Start Pathfinding / Re-plan
A	Toggle Algorithm (A* / GBFS)
H	Toggle Heuristic (Manhattan / Euclidean)
D	Toggle Dynamic Mode (ON/OFF)
R	Generate Random Walls
C	Clear Entire Grid
•	

import pygame
import math
import random
import heapq
import time

# --- Configuration & Constants ---
pygame.init()
pygame.font.init()

# Window Settings
GRID_SIZE = 600
UI_WIDTH = 250
WIDTH, HEIGHT = GRID_SIZE + UI_WIDTH, GRID_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Pathfinding Agent")

# Grid Settings
ROWS = 30
COLS = 30
NODE_WIDTH = GRID_SIZE // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
DARK_GREY = (100, 100, 100)
ORANGE = (255, 165, 0)      # Start
TURQUOISE = (64, 224, 208)  # Goal
YELLOW = (255, 255, 0)      # Frontier
RED = (255, 0, 0)           # Visited
GREEN = (0, 255, 0)         # Path
BLUE = (0, 0, 255)          # Agent
UI_BG = (40, 40, 40)
TEXT_COLOR = (255, 255, 255)

# Fonts
FONT = pygame.font.SysFont("Arial", 16)
TITLE_FONT = pygame.font.SysFont("Arial", 20, bold=True)

# --- Classes ---
class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.width = width
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_wall(self): return self.color == BLACK
    def is_start(self): return self.color == ORANGE
    def is_goal(self): return self.color == TURQUOISE

    def reset(self): self.color = WHITE
    def make_wall(self): self.color = BLACK
    def make_start(self): self.color = ORANGE
    def make_goal(self): self.color = TURQUOISE
    def make_visited(self): self.color = RED
    def make_frontier(self): self.color = YELLOW
    def make_path(self): self.color = GREEN
    def make_agent(self): self.color = BLUE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        pygame.draw.rect(win, GREY, (self.x, self.y, self.width, self.width), 1)

    def update_neighbors(self, grid):
        self.neighbors = []
        # Down, Up, Right, Left (No diagonals for simplicity, but can be added)
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_wall(): # Down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < COLS - 1 and not grid[self.row][self.col + 1].is_wall(): # Right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): # Left
            self.neighbors.append(grid[self.row][self.col - 1])

# --- Helper Functions ---
def h_manhattan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def h_euclidean(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse() # Start to Goal
    return path

def pathfinding(grid, start, goal, algo="A*", heuristic="Manhattan"):
    """
    Executes the pathfinding algorithm.
    algo: "A*" or "GBFS"
    heuristic: "Manhattan" or "Euclidean"
    """
    start_time = time.time()
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    # f_score is used differently based on algo
    f_score = {node: float("inf") for row in grid for node in row}
    h_func = h_manhattan if heuristic == "Manhattan" else h_euclidean
    f_score[start] = h_func(start.get_pos(), goal.get_pos())
    
    open_set_hash = {start}
    visited_nodes = 0

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == goal:
            end_time = time.time()
            path = reconstruct_path(came_from, goal)
            return path, visited_nodes, (end_time - start_time) * 1000

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            
            # A* cares about g_score. GBFS only cares about h_score.
            h_val = h_func(neighbor.get_pos(), goal.get_pos())
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                
                if algo == "A*":
                    f_score[neighbor] = temp_g_score + h_val
                else: # GBFS
                    f_score[neighbor] = h_val
                    
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_frontier()
                    visited_nodes += 1

        if current != start:
            current.make_visited()

    return [], visited_nodes, (time.time() - start_time) * 1000 # No path found

def generate_random_walls(grid, density=0.3):
    for row in grid:
        for node in row:
            if not node.is_start() and not node.is_goal() and random.random() < density:
                node.make_wall()

def draw_ui(win, state_vars):
    pygame.draw.rect(win, UI_BG, (GRID_SIZE, 0, UI_WIDTH, HEIGHT))
    
    labels = [
        ("ALGORITHM", TITLE_FONT, 20),
        (f"Current: {state_vars['algo']}", FONT, 50),
        ("Toggle Algo (Press A)", FONT, 70),
        
        ("HEURISTIC", TITLE_FONT, 120),
        (f"Current: {state_vars['heur']}", FONT, 150),
        ("Toggle Heuristic (Press H)", FONT, 170),
        
        ("DYNAMIC MODE", TITLE_FONT, 220),
        (f"Status: {'ON' if state_vars['dynamic'] else 'OFF'}", FONT, 250),
        ("Toggle Dynamic (Press D)", FONT, 270),
        
        ("CONTROLS", TITLE_FONT, 320),
        ("Left Click: Draw Wall", FONT, 350),
        ("Right Click: Erase", FONT, 370),
        ("Press R: Random Walls", FONT, 390),
        ("Press C: Clear Grid", FONT, 410),
        ("Press SPACE: Start/Replan", FONT, 430),
        
        ("METRICS", TITLE_FONT, 480),
        (f"Nodes Visited: {state_vars['visited']}", FONT, 510),
        (f"Path Cost: {state_vars['cost']}", FONT, 530),
        (f"Time: {state_vars['time']:.2f} ms", FONT, 550)
    ]
    
    for text, font, y_pos in labels:
        render = font.render(text, True, TEXT_COLOR)
        win.blit(render, (GRID_SIZE + 20, y_pos))

def clear_paths(grid):
    """Clears search visualization but keeps walls, start, and goal."""
    for row in grid:
        for node in row:
            if not node.is_wall() and not node.is_start() and not node.is_goal():
                node.reset()

def main():
    grid = [[Node(i, j, NODE_WIDTH) for j in range(COLS)] for i in range(ROWS)]
    
    # Fixed start and goal
    start = grid[2][2]
    goal = grid[ROWS - 3][COLS - 3]
    start.make_start()
    goal.make_goal()

    state_vars = {
        "algo": "A*",
        "heur": "Manhattan",
        "dynamic": False,
        "visited": 0,
        "cost": 0,
        "time": 0.0
    }

    run = True
    agent_path = []
    agent_moving = False
    agent_current_node = None

    clock = pygame.time.Clock()

    while run:
        # Draw everything
        WIN.fill(WHITE)
        for row in grid:
            for node in row:
                node.draw(WIN)
        
        # Draw agent if moving
        if agent_moving and agent_current_node:
            agent_current_node.make_agent()
            
        draw_ui(WIN, state_vars)
        pygame.display.update()

        # Dynamic Mode Logic (Agent Movement & Replanning)
        if agent_moving and len(agent_path) > 0:
            clock.tick(10) # Control agent speed
            
            # Spawn random walls if dynamic mode is on
            if state_vars["dynamic"] and random.random() < 0.1: # 10% chance per step
                empty_nodes = [n for row in grid for n in row if n.color == WHITE]
                if empty_nodes:
                    new_wall = random.choice(empty_nodes)
                    new_wall.make_wall()
                    
                    # RE-PLANNING: Check if new wall blocks the CURRENT remaining path
                    if new_wall in agent_path:
                        print("Obstacle detected on path! Replanning...")
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)
                        
                        clear_paths(grid)
                        start_replan = agent_current_node
                        start_replan.make_start()
                        
                        agent_path, v_nodes, exec_time = pathfinding(
                            grid, start_replan, goal, state_vars["algo"], state_vars["heur"]
                        )
                        
                        state_vars["visited"] = v_nodes
                        state_vars["cost"] = len(agent_path)
                        state_vars["time"] = exec_time
                        
                        for node in agent_path:
                            node.make_path()
                        
                        if not agent_path:
                            print("No valid path exists anymore!")
                            agent_moving = False

            # Move agent
            if agent_moving and len(agent_path) > 0:
                agent_current_node.make_path() # Restore path color behind it
                agent_current_node = agent_path.pop(0)
                agent_current_node.make_agent()
                
            if agent_current_node == goal:
                agent_moving = False
                print("Goal Reached!")

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Mouse drawing walls
            if pygame.mouse.get_pressed()[0]: # Left click
                pos = pygame.mouse.get_pos()
                if pos[0] < GRID_SIZE: # Ensure click is within grid
                    row, col = pos[1] // NODE_WIDTH, pos[0] // NODE_WIDTH
                    node = grid[row][col]
                    if node != start and node != goal:
                        node.make_wall()
            elif pygame.mouse.get_pressed()[2]: # Right click
                pos = pygame.mouse.get_pos()
                if pos[0] < GRID_SIZE:
                    row, col = pos[1] // NODE_WIDTH, pos[0] // NODE_WIDTH
                    node = grid[row][col]
                    if node != start and node != goal:
                        node.reset()

            # Keyboard Controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    state_vars["algo"] = "GBFS" if state_vars["algo"] == "A*" else "A*"
                if event.key == pygame.K_h:
                    state_vars["heur"] = "Euclidean" if state_vars["heur"] == "Manhattan" else "Manhattan"
                if event.key == pygame.K_d:
                    state_vars["dynamic"] = not state_vars["dynamic"]
                
                if event.key == pygame.K_r:
                    clear_paths(grid)
                    for row in grid:
                        for node in row:
                            if not node.is_start() and not node.is_goal():
                                node.reset()
                    generate_random_walls(grid, 0.3)
                    agent_moving = False

                if event.key == pygame.K_c:
                    for row in grid:
                        for node in row:
                            node.reset()
                            start.make_start()
                            goal.make_goal()
                    agent_moving = False

                if event.key == pygame.K_SPACE:
                    clear_paths(grid)
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    agent_path, v_nodes, exec_time = pathfinding(
                        grid, start, goal, state_vars["algo"], state_vars["heur"]
                    )
                    
                    state_vars["visited"] = v_nodes
                    state_vars["cost"] = len(agent_path)
                    state_vars["time"] = exec_time
                    
                    for node in agent_path:
                        node.make_path()
                        
                    if agent_path:
                        agent_moving = True
                        agent_current_node = start

    pygame.quit()

if __name__ == "__main__":
    main()
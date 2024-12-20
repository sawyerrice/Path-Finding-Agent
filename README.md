My search algorithm performs a breadth first search and tracks the value of paths and their endpoints relative to the goal state. To start, my algorithm adds the start state to a queue, and then adds all of the start states' possible single move actions into the queue to create a sort of first layer of moves within the queue. Then, this entire first layer is popped from the queue, and all of their children are added to create a second layer. This process repeats until a specified maximum depth is achieved. I toggle the maximum depth with a global variable to control how accurate or fast I want the algorithm to be. 

My breadth first search keeps track of several variables to help create a more informed search. Each object in the queue keeps track of the current position, the direction that the first step in the path took, the running score up to this specific location, the locations of the coins already collected up to current point, and the sequence of cells that were traversed to get to the current location.

As the search progresses, my algorithm is finding paths through all cells in the area near the starting state, and keeping track of the score that would be achieved if the agent took that specific path. Thus, the algorithm is actively tracking how many points have been accumulated by coins, how many points have been lost by making moves, and an estimate of how many points will be lost getting to the goal state. 

For each move, a new memory dictionary is created. My algorithm allows locations to be visited more than once as long as all visits to an already visited location increase the score from the previous maximum score of a path ending at that location. In other words, a new path can go through a location that is already visited, as long as the new path is more optimal than the previous path through the same location. If there are multiple ways to reach the same location, my algorithm will always choose the best path through that point.
    
If a specific path reaches the goal state, then the score of that path is whatever running score has been accumulated up to that point. This score is checked against a maximum path score for this individual move. If the path does not end at the goal state, the Manhattan distance to the goal state times two, times a constant $C$ is subtracted from the current score and this is treated as the score for this path. This heuristic can be tuned with $C$ to get the most accurate estimate of the actual distance from the goal state. At every single point across every single path, the current score minus the distance from goal estimation is checked against the max path so far. If the current path is estimated to achieve a greater score than the previous max path, then that max is stored along with the first move of that path. Ultimately, when the BFS returns, all that will be returned is the direction of the first move in the max path, and the sequence of locations that the max path traverses.

Because the entire max path is returned, I can control how many sequential moves the algorithm will take from each individual run of the BFS. Rather than running the BFS every single time I make a move, I instead have the choice of following the returned max path for a small number of moves, and then rerunning the BFS. This strategy drastically increases the speed of my algorithm and allows me to significantly increase the BFS layer depth. Further, this approach also prevents the agent from oscillating between two or three cells. If the agent has to follow 5 consecutive moves from the same path, it becomes very unlikely that two points on the map will tell the agent to follow the same inverse paths, and get stuck between those two points. However, if the agent is only following one move from the returned path, it is not unlikely that the agent will find itself in situations where point $a$ says the max path first goes through adjacent point $b$, and point $b$ says the max path from $b$ goes through adjacent point $a$.

# 2048_ai
AI that plays 2048

*PROGRAM WILL ONLY RUN IN PYTHON 2.7*

All code was provided to me except for playerAI.py. That is the file that contains everything related to the AI. The strategy this AI will use prioritizes stacking all the points in the lower right-hand corner of the board. It uses the minimax algorithm to plan 4 moves ahead and assume that the computer will place a new block in the most disadvantageous spot: as close to the lower right-hand corner as possible. To prioritze the lower right-hand corner, the AI uses a scoring system to determine the effectiveness of a move. It multiplies each tile value by a multiplier that corresponds to which diagonal of the board the tile is on and then adds all those values up. The multipliers are:

    4^0 4^1 4^2 4^3 
    4^1 4^2 4^3 4^4 
    4^2 4^3 4^4 4^5 
    4^3 4^4 4^5 4^6 
    
This way the AI will always prioritize making moves to make the lower right-hand corner a higher value.

To watch the AI play the game, run the GameManager.py file *USING PYTHON 2.7* and it will print the board each turn to the console.

# AR_Surviving-Seniors_sy625_yc823

Project title: **CornellTac**

Team members: Rachel Yan, Ian Chen

The project will implement an AI player to play the game of ultimate tic-tac-toe, which is a more complicated version of traditional tic-tac-toe, that is played on a 9x9 tile board on top of 9 different 3x3 games.

**Demo1 Demo Script:**
Rachel will be demonstrating the basic game play of the ultimate tic-tac-toe, which currently allows command-line interaction of two human players against each other. The game should generally be able to play, and there is also a command-line visualization of the game board. The TA should expect to see the code identifying the winner of the game based on how we played, some corner cases might still be incorrect, but most of the game should be played smoothly without error. To demo, go into the main folder and use command python3 game.py to start, and follow the text instruction and look at the printed board to finish the game. 

Ian will be demonstrating the backend minimax algorithm functions. In this part of the algorithm, test_empty_board ensures that the AI correctly selects a valid move when the voard is completely empty; test_x_xin_state checks that the Minimax algorithm correctly identifies a winning state for 'X'; test_tied_board ensures that the AI correctly identifies a tie state; test_alpha_beta_pruning checks that the Alpha-Beta pruning optimization works by ensuring the execution time is completed within 2 seconds, ensurs AI performs well under reasonable time constraints. These algorithmic implmentation checkings pave ways for furhter enhanced evaluation of tie and win, and reinforcement learning extension.

**Demo2 demo script**

Rachel Yan: Demonstrating the test cases, explain how each function is being tested to make sure that they are correct. TA should expect to see 24 test cases passing, with some others failing. We are still working on debugging for those failing test cases. To reproduce, please run the test program: python3 test_game.py

Ian Chen: Demonstrating the combing of the gameplay and the AI given, explain how the two modules are connected. And treatment to make the ai cleverer against human game play. TA should expect to see the following: A game played between a human player (O) and the AI (X), showing proper turn alternation and enforcement of rules. Dynamic board updates, winner announcements, and the correct application of the AI's moves. To reproduce, please follow the instructions below:
Run the main program: python main.py.
Follow on-screen prompts to input moves as the human player (O).
Observe the AI (X) making strategic moves.
Play until either a winner is declared or the game ends in a draw.
Verify the game enforces board restrictions (e.g., only allowing moves in the appropriate sub-board).

**Final demo script**
Check the requirements, especially for installing the correct version of pygame.

To demonstrate the game play, follow the following steps:
1. run the main program: python3 main.py
2. Follow the command line prompts to choose if playing using command line or playing using the gui with pygame.
3. Follow instruction of command line if using command line
4. GUI instructions
   1. Click on the buttons to choose between monte carlo algorithm or minimax algorithm to start
   2. Click on the grid you want to play in to play the human player, follow instructions of the subtitle at the bottom of the game window
   3. Play until either a winner is declared or the game ends in a draw

To demonstrate the correctness, run the test cases by python3 tests/test_game.py

There is no explicit demonstration on performance as we evaluated by running against human player and other algorithm by personally playing.

# COMP472-Assignment2
https://github.com/antoinePaulinB7/COMP472-Assignment2

## Instructions:
To run puzzles from the samples file:
* ```python -i solver.py```

To run an analysis on already solved puzzles
* ```python -i solver.py analyze```

To run solver on puzzles in existing file
* ```python -i solver.py [filename]```
* Example: ```python -i solver.py puzzles.txt```

To generate 50 puzzles and run solver on them
* ```python -i solver.py [filename]```
* The file name must be a new one, i.e. not an existing file
* Example: ```python -i solver.py generated-puzzles.txt```

To generate X puzzles and run solver on them
* ```python -i solver.py [filename] [X]```
* Example: ```python -i solver.py generated-puzzles.txt 15```

To demo the program (for the demo):
* ```python -i solver.py demo [filename]```
* Does the same thing as simply running solver on existing file, except it outputs to demo/ folder.
* Example: ```python -i solver.py demo the-demo-puzzles.txt```

To solve a single puzzle:
* ```python -i solver.py [filename] [X] [X] [X] [X] [X] [X] [X] [X]```
* Where ```[X] [X] [X] [X] [X] [X] [X] [X]``` is a valid puzzle. Outputs to the results folder with filename as the starting element of the files' titles.
* Example: ```python -i solver.py bobo.txt 1 2 4 3 5 6 7 0```
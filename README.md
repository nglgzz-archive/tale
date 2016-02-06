TALE
======
**TALE** is a program that shows the evolution of critters in a 2D world using neural networks mixed to an evolutionary algorithm.

## Brief explanation
This simulation is based on a 2D world containing critters and food randomly generated. Each critter has two neural networks, one responsible for the critter's movements and another one for reproduction. The neural networks' weights are randomly generated at first, then they change with backpropagation and from the second batch of critters onwards the weights are passed from the parents with a mutation.

At the moment after running the simulation with default settings two general behaviours are visible: in the first one the critters get extinct rather quickly, but some improvement in their survival skills is noticeable; in the other one they don't get extinct, the world gets overpopulated and their survival skills are pretty much non-existing, but they just reproduce a lot. 

## Dependencies
- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [Pygame 1.9.1](http://www.pygame.org/download.shtml)

## Usage
```
$ python graphics.py
```
Once running you can interact with the simulation in various ways. Here's the keys:
- space : start and pause
- tab : print some stats on the terminal (definitely have to improve this one)
- plus : increase time between each step
- minus : decrease time between each step (at a certain point the speed depends just on your pc power) 
- right arrow : move one step at the time
- s : save the brains of the current critters
- l : load the brains saved on the current critters (if the brains saved are too many some are not loaded, if they're too few they're not loaded onto each critter)
- backslash : insert command from terminal (at the moment commands are not parsed so it doesn't do anything)
- backspace : restart the simulation
- escape : quit the program

## Configuration
To change the parameters of the environment, graphics and critters you can edit the settings.py file, I tried to make it the most modular possible, so you can really change a lot of stuff there. 

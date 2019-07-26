# Music Generation

## Overview
Q-Learning is a model-free reinforcement learning algorithm that generates an optimal policy using a 
Markov decision process (MDP). The generated policy decides what action to take at a given game state by trying to maximize
the total reward over successive steps in the game.

Approximate Q-Learning uses a feature-based representation of the states instead of storing the Q-value for every game state 
the agent encounters. These Q-values are computed on demand, significantly reducing memory usage and time to train.

## Setup

### Prerequisites
* Python 3.5+
* numpy
* mido

### Training

Naive method: `python3 main.py`

Chord Heuristics and Hindsight: `python3 main2.py`

## Results

#### Naive
* TrialTwo.mid
* TrialThree.mid

#### Chord Heurisitcs and Hindsight
* NewCode.mid

## Team
| **Billy Wang**</a> | **Colton Nishida**</a> |
| :---: |:---:|
| [![Billy Wang](https://avatars1.githubusercontent.com/u/46856940?v=4&s=200)](https://github.com/albertczhang)    | [![Colton Nishida](https://avatars2.githubusercontent.com/u/46944125?v=4&s=200)](https://github.com/coltonnishida) |
| <a href="https://github.com/albertczhang" target="_blank">`github.com/albertczhang`</a> | <a href="https://github.com/coltonnishida" target="_blank">`github.com/coltonnishida`</a> |

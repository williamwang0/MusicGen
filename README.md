# Music Generation

## Overview
Music Generation analyzes midi files of various songs by a composer and generates a piece composed in a similar style. The project uses a Markov Decision Process (MDP) to determine how notes transitions from one to another.

In `main.py`, a naive Markov chain is implemented, only utilizing information about the previous note to determine which note to play next.

In `main2.py`, multiple previous notes are kept track of, resulting in a melody. In addition, major triads are artificially added.

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
| [![Billy Wang](https://avatars1.githubusercontent.com/u/46856940?v=4&s=200)](https://github.com/williamwang0)    | [![Colton Nishida](https://avatars2.githubusercontent.com/u/46944125?v=4&s=200)](https://github.com/coltonnishida) |
| <a href="https://github.com/williamwang0" target="_blank">`github.com/williamwang0`</a> | <a href="https://github.com/coltonnishida" target="_blank">`github.com/coltonnishida`</a> |

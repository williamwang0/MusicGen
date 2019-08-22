# Music Generation

## Overview
Music Generation analyzes the midi files of various pieces and generates a piece composed in a similar style. The project uses a Markov Decision Process (MDP) to determine how notes transitions from one to another.

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
* TrialOne.mid
* TrialTwo.mid
* TrialThree.mid

#### Chord Heurisitcs and Hindsight
* NewCode.mid

## Team
| **Albert Zhang**</a> | **Colton Nishida**</a> |
| :---: |:---:|
| [![Albert Zhang](https://avatars0.githubusercontent.com/u/31051641?v=4&s=200)](https://github.com/albertczhang) | [![Colton Nishida](https://avatars2.githubusercontent.com/u/46944125?v=4&s=200)](https://github.com/coltonnishida) |
| <a href="https://github.com/albertczhang" target="_blank">`github.com/albertczhang`</a> | <a href="https://github.com/coltonnishida" target="_blank">`github.com/coltonnishida`</a> |

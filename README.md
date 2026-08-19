# 💣 CS171 Artificial Intelligence: Minesweeper AI Agent
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)](file:///c:/Users/mannu/Downloads/Minesweeper-11-master/Minesweeper_Python)
[![C++](https://img.shields.io/badge/C++-11+-00599C?style=flat&logo=cplusplus&logoColor=white)](file:///c:/Users/mannu/Downloads/Minesweeper-11-master/Minesweeper_Cpp)
[![Java](https://img.shields.io/badge/Java-8+-007396?style=flat&logo=openjdk&logoColor=white)](file:///c:/Users/mannu/Downloads/Minesweeper-11-master/Minesweeper_Java)
[![Benchmark](https://img.shields.io/badge/Beginner%20Benchmark-1000%2F1000%20(100%25)-brightgreen)](#-performance--benchmarks)
[![Course](https://img.shields.io/badge/UC%20Irvine-CS%20171-blue)](file:///c:/Users/mannu/Downloads/Minesweeper-11-master/Minesweeper_Student_Manual.pdf)
An intelligent, multi-language constraint-satisfaction and probabilistic Minesweeper agent built for **CS 171 (Introduction to Artificial Intelligence)** at the **University of California, Irvine (UCI)**.
The framework supports complete agent environments in **Python**, **C++**, and **Java**, complete with world generators, automated batch evaluation, and interactive visual debugging modes.
---
## 📑 Table of Contents
- [Project Overview](#-project-overview)
- [Agent Architecture & Solver Logic](#-agent-architecture--solver-logic)
- [PEAS Framework Specification](#-peas-framework-specification)
- [Repository Structure](#-repository-structure)
- [Getting Started & Quick Run](#-getting-started--quick-run)
  - [Running the Python Agent](#running-the-python-agent)
  - [Compiling & Running C++](#compiling--running-c)
  - [Compiling & Running Java](#compiling--running-java)
- [World Generator](#-world-generator)
- [Performance & Benchmarks](#-performance--benchmarks)
- [Documentation & Course Artifacts](#-documentation--course-artifacts)
---
## 🌟 Project Overview
Minesweeper is a classic single-player puzzle game played on a grid. The goal of the AI agent is to uncover all safe cells on the board without detonating any hidden mines. Upon uncovering a cell, the environment returns a sensor value representing the number of adjacent mines ($0$ to $8$).
This repository provides:
1. **Fully Functioning Python AI (`MyAI.py`)**: Demonstrates a high-performance solver utilizing logical deduction, constraint satisfaction, and probabilistic guessing algorithms.
2. **Starter Templates in C++ and Java**: Standardized agent interfaces ready for extension.
3. **World Generator (`WorldGenerator.py`)**: Tooling for generating random boards with guaranteed safe starting locations across custom dimensions and mine counts.
4. **Comprehensive Evaluation Suite**: Utilities to run single-board tests or bulk evaluations across thousands of problem instances.
---
## 🧠 Agent Architecture & Solver Logic
The Python solver ([`MyAI.py`](file:///c:/Users/mannu/Downloads/Minesweeper-11-master/Minesweeper_Python/src/MyAI.py)) combines deterministic logic with probabilistic decision-making:
```
                  +----------------------------------+
                  |         Receive Sensor           |
                  |     (Adjacent Mine Count)        |
                  +-----------------+----------------+
                                    |
                                    v
                  +----------------------------------+
                  |   Level 1: Single-Cell Inference |
                  |   - Hint == Covered + Flags => Flag|
                  |   - Hint == Flags => Safe Uncover  |
                  +-----------------+----------------+
                                    | (If no move found)
                                    v
                  +----------------------------------+
                  | Level 2: Subset Deduction        |
                  | - Set difference: Cov(B) - Cov(A)|
                  | - Infer safe tiles / flags       |
                  +-----------------+----------------+
                                    | (If no move found)
                                    v
                  +----------------------------------+
                  | Level 3: Total Mine Constraint   |
                  | - If Flags == TotalMines:        |
                  |   Uncover all remaining covered  |
                  +-----------------+----------------+
                                    | (If no move found)
                                    v
                  +----------------------------------+
                  | Level 4: Probabilistic Guessing  |
                  | - Calculate Frontier Cell Risk   |
                  | - Calculate Global Cell Risk     |
                  | - Pick Lowest-Risk Tile (Corners)|
                  +----------------------------------+
```
1. **Single-Cell Local Inference**:
   - If `Hint == CoveredNeighbors + FlaggedNeighbors`, all unflagged neighbors are guaranteed **mines** $\rightarrow$ Flag them.
   - If `Hint == FlaggedNeighbors`, all remaining covered neighbors are guaranteed **safe** $\rightarrow$ Uncover them.
2. **Subset & Overlapping Constraint Reduction**:
   - Evaluates pairs of boundary cells $(A, B)$ where Covered Neighbors of $A \subseteq$ Covered Neighbors of $B$.
   - Calculates effective remaining mines for each set ($\text{Eff} = \text{Hint} - \text{Flags}$).
   - If $\text{Eff}(B) - \text{Eff}(A) == 0$, the set difference $B \setminus A$ contains **only safe tiles**.
   - If $\text{Eff}(B) - \text{Eff}(A) == |B \setminus A|$, the set difference $B \setminus A$ contains **only mines**.
3. **Global Mine Count Constraint**:
   - When total flagged mines match `totalMines`, all remaining covered grid squares are marked safe for instant uncovering.
4. **Probabilistic Minimum-Risk Guessing**:
   - When no deterministic move exists, the agent calculates mine probability across frontier cells ($\text{Risk} = \text{Eff} / |\text{Covered}|$) and un-frontiered global tiles ($\text{RemainingMines} / |\text{CoveredTotal}|$).
   - Prioritizes opening un-frontiered **corner tiles** or minimum-risk frontier tiles to minimize loss probability.
---
## 🎯 PEAS Framework Specification
|
 PEAS Component 
|
 Description 
|
|
:---
|
:---
|
|
**
Performance Measure
**
|
 +1 point for each successfully solved world; 0 points for hit mines / incomplete worlds. Score maximized across tournament runs. 
|
|
**
Environment
**
|
 Grid of size $R \times C$ containing $M$ hidden mines. Single guaranteed safe start patch. 
|
|
**
Actuators
**
|
 Actions returned by 
`getAction()`
: 
`UNCOVER(x, y)`
, 
`FLAG(x, y)`
, 
`UNFLAG(x, y)`
, 
`LEAVE`
 (for forfeiting/ending). 
|
|
**
Sensors
**
|
 Integer count ($0 \le N \le 8$) of adjacent mines returned after an 
`UNCOVER`
 action. Returns $-1$ for non-uncover actions. 
|
---
## 📁 Repository Structure
```
Minesweeper-11-master/
├── README.md                          # Project documentation
├── Minesweeper_Student_Manual.pdf     # CS171 assignment specification & student guide
├── Minesweeper_Final_AI_Report.docx   # Final project report template & performance rubric
│
├── Minesweeper_Python/                # Python Agent Implementation
│   ├── Makefile                       # Build and run commands
│   └── src/
│       ├── Main.py                    # CLI entry point, argument parser, test runner
│       ├── MyAI.py                    # Intelligent Minesweeper Solver (Constraint & Probabilistic)
│       ├── World.py                   # Game engine simulation & scoring logic
│       ├── AI.py                      # Abstract base agent class
│       ├── Action.py                  # Action data types (UNCOVER, FLAG, UNFLAG, LEAVE)
│       ├── RandomAI.py                # Baseline random action agent
│       └── ManualAI.py                # Interactive manual player mode
│
├── Minesweeper_Cpp/                   # C++ Starter Framework
│   ├── Makefile                       # C++ Makefile target
│   └── src/                           # MyAI.cpp, MyAI.hpp, World.cpp, Main.cpp
│
├── Minesweeper_Java/                  # Java Starter Framework
│   ├── Makefile                       # Java Makefile target
│   ├── manifest.txt                   # JAR build manifest
│   ├── jars/                          # Java executable dependencies
│   └── src/                           # MyAI.java, World.java, Main.java
│
└── WorldGenerator/                    # Problem Generation Tooling
    ├── WorldGenerator.py              # Script to generate custom .txt world files
    ├── generateSuperEasy.sh           # Shell script for easy benchmark generation
    ├── generateTournament.sh          # Shell script for tournament suite generation
    └── Problems/                      # 1,000 pre-generated Beginner test worlds (Easy1.txt..Easy1000.txt)
```
---
## 🚀 Getting Started & Quick Run
### Prerequisites
- **Python 3.6+**
- **G++ / GCC** (Optional, for C++ build)
- **JDK 8+** (Optional, for Java build)
---
### Running the Python Agent
Navigate to the `Minesweeper_Python` folder:
```bash
cd Minesweeper_Python
```
#### 1. Evaluate Agent on All 1,000 Benchmark Problems
```bash
python src/Main.py -f ../WorldGenerator/Problems
```
#### 2. Run a Single Problem File with Debug Board Output
```bash
python src/Main.py -f ../WorldGenerator/Problems/Easy1.txt -d
```
#### 3. Play Manually (Interactive Mode)
```bash
python src/Main.py -m
```
#### 4. Run Baseline Random Agent
```bash
python src/Main.py -r
```
#### CLI Command Options Reference (`Main.py`)
- `-f [InputPath] [OutputFile]` : Specify input world file or folder of world files. Optionally write results to an output text file.
- `-d` : Enable **Debug Mode** (prints ASCII game board after every move).
- `-v` : Enable **Verbose Mode** (prints file names before executing each world).
- `-m` : Enable **Manual Mode** (play the game via keyboard input).
- `-r` : Run **Random AI** baseline.
---
### Compiling & Running C++
Navigate to `Minesweeper_Cpp`:
```bash
cd Minesweeper_Cpp
make
./bin/Minesweeper -f ../WorldGenerator/Problems
```
---
### Compiling & Running Java
Navigate to `Minesweeper_Java`:
```bash
cd Minesweeper_Java
make
java -jar jars/Minesweeper.jar -f ../WorldGenerator/Problems
```
---
## 🛠 World Generator
Generate custom Minesweeper world files of any grid size or mine count using `WorldGenerator.py`:
```bash
cd WorldGenerator
python WorldGenerator.py <numFiles> <baseFilename> <rowDimension> <colDimension> <numMines>
```
### Example
Generate 100 Medium boards ($8 \times 8$ grid with $10$ mines):
```bash
python WorldGenerator.py 100 Medium 8 8 10
```
Constraints: `rowDimension >= 4`, `colDimension >= 4`, `1 <= numMines <= (rows * cols - 9)`.
---
## 📊 Performance & Benchmarks
Evaluation results for [`MyAI.py`](file:///c:/Users/mannu/Downloads/Minesweeper-11-master/Minesweeper_Python/src/MyAI.py) on the 1,000 pre-generated Beginner test suite:
|
 Board Category 
|
 Dimensions 
|
 Mines 
|
 Sample Size 
|
 Solved / Total 
|
 Win Rate 
|
|
:---
|
:---:
|
:---:
|
:---:
|
:---:
|
:---:
|
|
**
Beginner / Easy
**
|
 $8
|
 10 
|
 1,000 worlds 
|
**
1,000 / 1,000
**
|
**
100.0%
**
 🎯 
|
---
## 📚 Documentation & Course Artifacts
- [📄 Student Manual PDF](file:///c:/Users/mannu/Downloads/Minesweeper-11-master/Minesweeper_Student_Manual.pdf): Official UC Irvine CS171 assignment documentation detailing tournament rules, board representation, and environment constraints.
- [📝 Final AI Report DOCX](file:///c:/Users/mannu/Downloads/Minesweeper-11-master/Minesweeper_Final_AI_Report.docx): Submission template for benchmark summaries across 5x5, 8x8, 16x16, and 16x30 grid configurations.
---
*Developed as part of CS 171 (Intro to AI) at UC Irvine.*

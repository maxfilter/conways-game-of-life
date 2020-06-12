# Conway's Game of Life

This repository contains a visualization of Conway's Game of Life which uses color to represent age. The window is a PyQt5 widget.

**Python Dependencies:** `PyQt5` `numpy` `random`

## Rules

Conway's game of life is a grid of cells, which live and die based on the following set of rules (as per Wikipedia):

1.  Any live cell with fewer than two live neighbors dies, as if by
    underpopulation.
2.  Any live cell with two or three live neighbors lives on to the
    next generation.
3.  Any live cell with more than three live neighbors dies, as if by
    overpopulation.
4.  Any dead cell with exactly three live neighbors becomes a live cell, 
    as if by reproduction.

## Visualization

![Game of Life Demo](figures/cgol.gif)

#!/bin/bash

# Run this with https://github.com/percyliang/brown-cluster

# One text file containing the corpus
# We used the first 9999 entries of wikipedia
CORPUS=$1

# The number of clusters:
NCLUSTERS=3700

./wcluster --text $CORPUS  --c $NCLUSTERS


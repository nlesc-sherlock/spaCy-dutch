#!/bin/bash
###################################################
# This script creates the vocab data for a language.
# Usage:
# createvocab.sh path/to/temp path/to/corpus outputpath
###################################################

###################################################
# Parameters
###################################################

#Location of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# absolute path where all intermediate results are stored
TEMP=$(pwd)/temp

# Path to corpus directory, containing one file for each document.
# These documents will be tokenized with spacy's tokenizer
CORPUS_DIR=$1

# Path to directory with input files. This should contain the following:
#        * prefix.txt
#        * suffix.txt
#        * infix.txt
#        * morphs.json
#        * specials.json
#       * gazetteer.json
#       * tagmap.json
#       * lemma_rules.json
INPUTPATH=$2

# Output path where the vocab data will be stored
OUTPUTPATH=$3

# Nr of brown clusters to train
NCLUSTERS=100
# Vector length for word2vec - 300
VECTOR_SIZE=300
# Window size for word2vec
WINDOW_SIZE=5

# Which steps are executed
BROWN=1
WORD2VEC=1
FREQS=1

LANG_ID=nl

###################################################
# Preparation
###################################################
mkdir -p $TEMP/$LANG_ID/
cp $INPUTPATH/* $TEMP/$LANG_ID/

###################################################
# Build corpus file
###################################################
echo "Build the corpus file..."
CORPUS=$TEMP/corpus.txt
python $DIR/build_corpusfile.py $LANG_ID $CORPUS_DIR $CORPUS

###################################################
# Brown Clusters
# Clone and compile the code from github for brown clustering
# Then run it on the corpus
###################################################
if (($BROWN > 0));  then
    echo "Training brown clusters..."
    mkdir -p $TEMP/brown
    git clone https://github.com/percyliang/brown-cluster
    cd brown-cluster
    make
    ./wcluster --text $CORPUS  --c $NCLUSTERS --output_dir $TEMP/brown
    cp $TEMP/brown/paths $TEMP/$LANG_ID/clusters.txt
    cd ..
    rm -rf brown-cluster
    rm $CORPUS.int $CORPUS.strdb
 fi

###################################################
# Word2vec vector creation
# Clones and builds the code for GloVe
###################################################
# Some settings for glove
COOCCURRENCE_FILE=cooccurrence.bin
COOCCURRENCE_SHUF_FILE=cooccurrence.shuf.bin
# This is the build directory of GloVe:
BUILDDIR=build
SAVE_FILE=vectors
VERBOSE=2
MEMORY=4.0
VOCAB_FILE=vocab.txt
VOCAB_MIN_COUNT=5
MAX_ITER=15
BINARY=2
NUM_THREADS=8
X_MAX=10

if (($WORD2VEC > 0));  then
    echo "Training word2vec..."
    #mkdir $TEMP/vectors
    git clone https://github.com/stanfordnlp/GloVe glove/
    cd glove
    make

    # The code below is more or less copied from the demo file in glove
    $BUILDDIR/vocab_count -min-count $VOCAB_MIN_COUNT -verbose $VERBOSE < $CORPUS > $VOCAB_FILE
    if [[ $? -eq 0 ]]
      then
      $BUILDDIR/cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $CORPUS > $COOCCURRENCE_FILE
      if [[ $? -eq 0 ]]
      then
        $BUILDDIR/shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE
        if [[ $? -eq 0 ]]
        then
           $BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE
           if [[ $? -eq 0 ]]
           then
               python eval/python/evaluate.py
           fi
        fi
      fi
    fi

    # Compress and move the results
    bzip2 vectors.txt
    cd ..
    mv glove/vectors.txt.bz2 $TEMP/$LANG_ID/vectors.bz2
    rm -rf glove
fi


###################################################
# Count frequencies
###################################################
if (($FREQS > 0));  then
    echo "Counting frequencies..."
    python $DIR/count_frequencies.py $LANG_ID $CORPUS_DIR $TEMP/$LANG_ID
    gzip $TEMP/$LANG_ID/freqs.txt
fi


###################################################
# Create the actual vocab data
###################################################
echo "Creating the vocab data..."
python $DIR/init_model.py $LANG_ID $TEMP $TEMP $OUTPUTPATH


###################################################
# Clean up
###################################################
echo "Done, copied all results to $OUTPUTPATH"
#rm -rf $TEMP
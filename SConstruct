import os
import os.path
import logging
import random
import subprocess
import shlex
import gzip
import re
import functools
import time
import imp
import sys


# Variables control various aspects of the experiment.  Note that you have to declare
# any variables you want to use here, with reasonable default values, but when you want
# to change/override the default values, do so in the "custom.py" file (see it for an
# example, changing the number of folds).
vars = Variables("custom.py")
vars.AddVariables(
    ("MODEL_TYPES", "", ["roberta-base", "bert-base-cased"]), #the embedding model to use to calculate anthroscore
    ("DATASETS", "", {"acl_50" : "replication/acl_50.csv"}), #a dictionary of datasetname: location of dataset for each dataset to get AS for
    ("DEP_INCLUDE","", ["nsubj", "dobj"]), #Noun dependencies to include
    ("TARGET_WORDS","", "replication/entities.txt"), #Target word list. Will be ignored for unsupervised
    ("ANIMATE_PRONOUNS", "", ["he", "she", "her", "him", "He", "She", "Her"]), #List of animate pronouns
    ("INANIMATE_PRONOUNS", "", ["it","its","It","Its"]), #List of inanimate pronouns
    ("UNSUPERVISED", "", [False, True]), #If false, use word list. Otherwise, use all nouns.
    ("DEVICE", "", "cpu")
)

# Methods on the environment object are used all over the place, but it mostly serves to
# manage the variables (see above) and builders (see below).
env = Environment(
    variables=vars,
    ENV=os.environ,
    
    # Defining a bunch of builders (none of these do anything except "touch" their targets,
    # as you can see in the dummy.py script).  Consider in particular the "TrainModel" builder,
    # which interpolates two variables beyond the standard SOURCES/TARGETS: PARAMETER_VALUE
    # and MODEL_TYPE.  When we invoke the TrainModel builder (see below), we'll need to pass
    # in values for these (note that e.g. the existence of a MODEL_TYPES variable above doesn't
    # automatically populate MODEL_TYPE, we'll do this with for-loops).
    BUILDERS={
        "CreateData" : Builder(
            action="python scripts/file_read.py --input ${SOURCES[0]} --outputs ${TARGETS[0]}"
        ),
        "GetAS" : Builder(
            action="python scripts/embeddings.py --input ${SOURCES[0]} --outputs ${TARGETS[0]} "
            "--dep_include ${DEP_INCLUDE} --animate_pronouns ${ANIMATE_PRONOUNS} "
            "--inanimate_pronouns ${INANIMATE_PRONOUNS} --target_words ${TARGET_WORDS} "
            "--device ${DEVICE} --model ${MODEL}"
        ),
        "GetASUnsup" : Builder(
            action="python scripts/embeddings.py --input ${SOURCES[0]} --outputs ${TARGETS[0]} "
            "--dep_include ${DEP_INCLUDE} --animate_pronouns ${ANIMATE_PRONOUNS} "
            "--inanimate_pronouns ${INANIMATE_PRONOUNS} --target_words ${TARGET_WORDS} "
            "--device ${DEVICE} --model ${MODEL} --all_nouns"
        )
    }
)

# OK, at this point we have defined all the builders and variables, so it's
# time to specify the actual experimental process, which will involve
# running all combinations of datasets, folds, model types, and parameter values,
# collecting the build artifacts from applying the models to test data in a list.
#
# The basic pattern for invoking a build rule is:
#
#   "Rule(list_of_targets, list_of_sources, VARIABLE1=value, VARIABLE2=value...)"
#
# Note how variables are specified in each invocation, and their values used to fill
# in the build commands *and* determine output filenames.  It's a very flexible system,
# and there are ways to make it less verbose, but in this case explicit is better than
# implicit.
#
# Note also how the outputs ("targets") from earlier invocation are used as the inputs
# ("sources") to later ones, and how some outputs are also gathered into the "results"
# variable, so they can be summarized together after each experiment runs.
results = []
for dataset_name, dataset_file in env["DATASETS"].items():
    data = env.CreateData("work/${DATASET_NAME}/data.gz.jsonl", dataset_file, DATASET_NAME=dataset_name)
    for unsup in env["UNSUPERVISED"]:
        for model_type in env["MODEL_TYPES"]:
            if unsup:
               a_scores = env.GetASUnsup("work/${DATASET_NAME}/${MODEL}/all_nouns/as.gz.jsonl", data, DATASET_NAME=dataset_name, MODEL=model_type)
            else:
                a_scores = env.GetAS("work/${DATASET_NAME}/${MODEL}/wordlist/as.gz.jsonl", data, DATASET_NAME=dataset_name, MODEL=model_type)

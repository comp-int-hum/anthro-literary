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

#"acl_50" : "replication/acl_50.csv",
#replication/entities.txt"


# Variables control various aspects of the experiment.  Note that you have to declare
# any variables you want to use here, with reasonable default values, but when you want
# to change/override the default values, do so in the "custom.py" file (see it for an
# example, changing the number of folds).
vars = Variables("custom.py")
vars.AddVariables(
    ("MODEL_TYPES", "", ["roberta-base", "bert-base-cased"]), #the embedding model to use to calculate anthroscore
    ("DATASETS", "", {"gutenberg" : "data/gutenberg-lines.jsonl"}), #a dictionary of datasetname: location of dataset for each dataset to get AS for
    ("DEP_INCLUDE","", ["nsubj", "dobj"]), #Noun dependencies to include
    ("TARGET_WORDS","", ["tree","pen","rock"]), #Target word list. Will be ignored for unsupervised
    ("ANIMATE_PRONOUNS", "", ["he", "she", "her", "him", "He", "She", "Her"]), #List of animate pronouns
    ("INANIMATE_PRONOUNS", "", ["it","its","It","Its"]), #List of inanimate pronouns
    #("UNSUPERVISED", "", [False, True]), #If false, use word list. Otherwise, use all nouns.
    ("UNSUPERVISED", "", [False]),
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
        ),
        "TotalMeanAuthor": Builder(
            action="python scripts/total_mean_author.py ${SOURCES[0]} ${TARGETS[0]}"
        ),
        "TotalMeanWord": Builder(
            action="python scripts/total_mean_word.py ${SOURCES[0]} ${TARGETS[0]}"
        ),
        #stats.py, in embeddings, out ratio of pos/neg scores
        "PosNegRatio": Builder(
            action="python scripts/stats.py ${SOURCES[0]} ${TARGETS[0]}"
        ),
        #score_compare.py absolute difference of anthroscores across models, pointwise (delta of individual scores)
        #mean_diff.py takes mean of column for score_compare
        #compare_stats.py distribution measures etc, pointwise
        

        #score_counts.py bucketing, takes each model output, score_dist.py, perc. bucketing
        "BucketScores" : Builder(
            action="python scripts/score_counts.py ${SOURCES[0]} ${TARGETS[0]}"
        ),
        #model_negatives.py pull all negative scores
        "ModelNegatives" : Builder(
            action="python scripts/model_negatives.py ${SOURCES[0]} ${TARGETS[0]} --thresh 0"
        ),

        "WordVerb" : Builder(
            action="python scripts/word_verb_score.py --input ${SOURCES[0]} --output_wv ${TARGETS[0]} --output_avw ${TARGETS[1]}"
        ),

        #author_verbs complex: All verbs/sentence/author. Gather with Ascore > 1. Are there verbs that are particularly associated with target being high/author?


        #verbs_author_mean.py: Mean score per verb per author, all verbs
        "HumanReadable" : Builder(
            action="python scripts/csv_readable.py --input ${SOURCES[0]} --outputs ${TARGETS[0]}"),
        "SplitTargets" : Builder(
            action="python scripts/split_by_target.py --input ${SOURCES[0]} --outputs ${TARGETS[0]} --col ${COL}"
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
results_sup = {}
results_un = {}
individual_model = {mname: [] for mname in env["MODEL_TYPES"]}

for dataset_name, dataset_file in env["DATASETS"].items():
    data = env.CreateData("work/${DATASET_NAME}/data.gz.jsonl", dataset_file, DATASET_NAME=dataset_name)
    for unsup in env["UNSUPERVISED"]:
        oname = "all_nouns" if unsup else "wordlist"
        for model_type in env["MODEL_TYPES"]:
            if unsup:
               a_scores = env.GetASUnsup("work/${DATASET_NAME}/${MODEL}/${ONAME}/as.gz.jsonl", data, DATASET_NAME=dataset_name, MODEL=model_type, ONAME=oname)
               results_un[model_type] = a_scores
            else:
               a_scores = env.GetAS("work/${DATASET_NAME}/${MODEL}/${ONAME}/as.gz.jsonl", data, DATASET_NAME=dataset_name, MODEL=model_type, ONAME=oname)
               results_sup[model_type] = a_scores
            csv_out = env.HumanReadable("work/${DATASET_NAME}/${MODEL}/${ONAME}/readable.csv", a_scores, DATASET_NAME=dataset_name, MODEL=model_type, ONAME=oname)
            total_mean_a = env.TotalMeanAuthor("work/${DATASET_NAME}/${MODEL}/${ONAME}/total_mean_author.csv", a_scores, DATASET_NAME=dataset_name, MODEL=model_type, ONAME=oname)
            total_mean_w = env.TotalMeanWord("work/${DATASET_NAME}/${MODEL}/${ONAME}/total_mean_word.csv", a_scores, DATASET_NAME=dataset_name, MODEL=model_type, ONAME=oname)
            pos_neg = env.PosNegRatio("work/${DATASET_NAME}/${MODEL}/${ONAME}/pos_neg.csv", a_scores, DATASET_NAME=dataset_name, MODEL=model_type, ONAME=oname)
            score_buckets = env.BucketScores("work/${DATASET_NAME}/${MODEL}/${ONAME}/score_buckets.csv", a_scores, DATASET_NAME=dataset_name, MODEL=model_type, ONAME=oname)
            negatives = env.ModelNegatives("work/${DATASET_NAME}/${MODEL}/${ONAME}/negatives.csv", a_scores, DATASET_NAME=dataset_name, MODEL=model_type, ONAME=oname)

    for model_type, a_s in results_sup.items():
        for col in env["TARGET_WORDS"]:
            indy_res = env.SplitTargets("work/${DATASET_NAME}/${MODEL}/individual/${COL}.gz.jsonl", a_s, DATASET_NAME=dataset_name, MODEL=model_type, COL=col)
            individual_model[model_type].append(indy_res)           
            csv_out = env.HumanReadable("work/${DATASET_NAME}/${MODEL}/individual/${COL}_readable.csv", indy_res, DATASET_NAME=dataset_name, MODEL=model_type, COL=col)
            total_mean_a = env.TotalMeanAuthor("work/${DATASET_NAME}/${MODEL}/individual/${COL}_total_mean_author.csv", indy_res, DATASET_NAME=dataset_name, MODEL=model_type, COL=col)
            total_mean_w = env.TotalMeanWord("work/${DATASET_NAME}/${MODEL}/individual/${COL}_total_mean_word.csv", indy_res, DATASET_NAME=dataset_name, MODEL=model_type, COL=col)
            pos_neg = env.PosNegRatio("work/${DATASET_NAME}/${MODEL}/individual/${COL}_pos_neg.csv", indy_res, DATASET_NAME=dataset_name, MODEL=model_type, COL=col)
            score_buckets = env.BucketScores("work/${DATASET_NAME}/${MODEL}/individual/${COL}_score_buckets.csv", indy_res, DATASET_NAME=dataset_name, MODEL=model_type, COL=col)
            negatives = env.ModelNegatives("work/${DATASET_NAME}/${MODEL}/individual/${COL}_negatives.csv", indy_res, DATASET_NAME=dataset_name, MODEL=model_type, COL=col)
            word_verb = env.WordVerb(["work/${DATASET_NAME}/${MODEL}/individual/${COL}_verb_score.csv","work/${DATASET_NAME}/${MODEL}/individual/${COL}_author_verb_score.csv"], indy_res, DATASET_NAME=dataset_name, MODEL=model_type, COL=col)


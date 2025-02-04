import argparse
import gzip
import json
import csv
import pandas as pd
from scipy import stats

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--bert_in", help = "gz.jsonl with bert embeddings")
	parser.add_argument("--roberta_in", help = "gz.jsonl with roberta embeddings")
	parser.add_argument("--stats_out", help = "csv with statistics")

	args = parser.parse_args()

	with gzip.open(args.bert_in, "rt") as b_in, gzip.open(args.roberta_in, "rt") as r_in:
		bert_loaded_json = [{"score": json.loads(line)["score"]} for line in b_in]
		rob_loaded_json = [{"score": json.loads(line)["score"]} for line in r_in]
		bert_df = pd.DataFrame(bert_loaded_json)
		rob_df = pd.DataFrame(rob_loaded_json)

		bert_df["score"] = pd.to_numeric(bert_df["score"], errors="coerce")
		rob_df["score"] = pd.to_numeric(rob_df["score"], errors="coerce")

		bert_df["score"].dropna()
		rob_df["score"].dropna()

		bert_mean, bert_var, bert_std = stats.mvsdist(bert_df["score"])
		rob_mean, rob_var, rob_std = stats.mvsdist(rob_df["score"])
		correlation, p_val = stats.pearsonr(rob_df["score"], bert_df["score"])

		print(bert_mean.std())

		out_df["BERT distribution"] = ["mean" + str(bert_mean.mean()), "variance" + str(bert_mean.interval()), "standard deviation" + str(bert_mean.std())]
		out_df["RoBERTa distribution"] = ["mean" + str(rob_mean.mean()), "variance" + str(rob_mean.interval()), "standard deviation" + str(rob_mean.std())]
		out_df["correlation"] = ["correlation" + str(correlation), "p value" + str(p_val)]

		out_df.to_csv(args.stats_out)

import argparse
import gzip
import json
import csv
import pandas as pd
from scipy import stats

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("bert_in", help = "gz.jsonl with bert embeddings")
	parser.add_argument("roberta_in", help = "gz.jsonl with roberta embeddings")
	parser.add_argument("stats_out", help = "csv with statistics")

	args = parser.parse_args()

	bert_df = pd.read_json(args.bert_in, lines=True, compression="gzip")
	rob_df = pd.read_json(args.roberta_in, lines=True, compression="gzip")

	bert_df["score"] = pd.to_numeric(bert_df["score"], errors="coerce")
	rob_df["score"] = pd.to_numeric(rob_df["score"], errors="coerce")

	bert_mean, bert_var, bert_std = stats.mvsdist(bert_df["score"])
	rob_mean, rob_var, rob_std = stats.mvsdist(rob_df["score"])
	correlation, p_val = stats.pearsonr(rob_df["score"], bert_df["score"])

	out_df = pd.DataFrame()
	print("done")

	out_df["BERT distribution"] = ["mean" + bert_mean, "variance" + bert_var, "standard deviation" + bert_std]
	out_df["RoBERTa distribution"] = ["mean" + rob_mean, "variance" + rob_var, "standard deviation" + rob_std]
	out_df["correlation"] = ["correlation" + correlation, "p value" + p_val]

	out_df.to_csv(args.stats_out)

#	with gzip.open(args.bert_in, "rt") as bert_in, gzip.open(args.roberta_in, "rt") as rob_in, open(args.stats_out, "wt") as s_out:
#		out_writer = csv.writer(s_out)
#		out_writer.writerow(["variance", "correlation"])
#		for b_line, r_line in zip(bert_in, rob_in):
#			bert_line = json.loads(b_line)
#			rob_line = json.loads(r_line)
#			print(bert_line["score"])
#			bert_mean, bert_var, bert_std = stats.mvsdist(bert_line["score"])
#			rob_mean, rob_var, rob_std = stats.mvsdist(rob_line["score"])
#			correlation, p_val = stats.pearsonr(rob_line["score"], bert_line["score"])
#			out_writer.writerow({"bert mean": bert_mean, "roberta mean": rob_mean, "bert variance": bert_var, "roberta variance": rob_var, "bert standard deviation": bert_std, "roberta standard deviation": rob_std, "correlation": correlation, "p value": p_val} + "\n")

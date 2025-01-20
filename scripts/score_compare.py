import argparse
import gzip
import json
import csv
import pandas as pd

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("bert_in", help = "gz.jsonl with bert embeddings")
	parser.add_argument("roberta_in", help = "gz.jsonl with roberta embeddings")
	parser.add_argument("score_out", help = "csv with score difference")

	args = parser.parse_args()


	with gzip.open(args.bert_in, "rt") as b_in, gzip.open(args.roberta_in, "rt") as r_in:
		bert_loaded_json = [{"score": json.loads(line)["score"]} for line in b_in]
		rob_loaded_json = [{"score": json.loads(line)["score"]} for line in r_in]
		bert_df = pd.DataFrame(bert_loaded_json)
		rob_df = pd.DataFrame(rob_loaded_json)

		bert_df.groupby("score")
		rob_df.groupby("score")

		scores = {"BERT": bert_df["score"], "RoBERTa": rob_df["score"]}
		df = pd.DataFrame(data=scores)
		df["BERT"] = pd.to_numeric(df["BERT"], errors="coerce")
		df["RoBERTa"] = pd.to_numeric(df["RoBERTa"], errors="coerce")
		df["difference"] = df["BERT"] - df["RoBERTa"]
		df["difference"] = df["difference"].abs()

		df.to_csv(args.score_out)

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

	bdf = pd.read_json(args.bert_in, lines=True, compression="gzip")
	rdf = pd.read_json(args.roberta_in, lines=True, compression="gzip")

	bdf.groupby("score")
	rdf.groupby("score")
#	bdf.rename(columns={"score": "BERT"})
#	rdf.rename(columns={"score": "RoBERTa"})
#	bdf = bdf[["sentence", "word", "score"]]
#	rdf = rdf[["sentence", "word", "score"]]

#	sdf = bdf.merge(rdf)
#	sdf["difference"] = sdf["BERT"].abs() - sdf["RoBERTa"].abs()
	scores = {"BERT": bdf["score"], "RoBERTa": rdf["score"]}
	df = pd.DataFrame(data=scores)
	df["BERT"] = pd.to_numeric(df["BERT"], errors="coerce")
	df["RoBERTa"] = pd.to_numeric(df["RoBERTa"], errors="coerce")
	df["difference"] = df["BERT"] - df["RoBERTa"]
	df["difference"] = df["difference"].abs()

#	print(bdf.abs().max())
#	print(rdf.abs().max())

	df.to_csv(args.score_out)

import argparse
import gzip
import json
import csv
import pandas as pd
import math

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help = "gz.jsonl with verb frequencies")
	parser.add_argument("stats_out", help = "csv with statistics on frequency")

	args = parser.parse_args()

	df = pd.read_json(args.verbs_in, lines=True, compression="gzip")

	df["score"] = pd.to_numeric(df["score"], errors="coerce")
	null = df["score"] [(df["score"] >= 0) & (df["score"] < 1)]
	decimals = null.count()
	eins = df["score"] [(df["score"] >= 1) & (df["score"] < 2)]
	one = eins.count()
	zwei = df["score"] [(df["score"] >= 2) & (df["score"] < 3)]
	two = zwei.count()
	drei = df["score"] [(df["score"] >= 3) & (df["score"] < 4)]
	three = drei.count()
	vier = df["score"] [(df["score"] >= 4) & (df["score"] < 5)]
	four = vier.count()
	funf = df["score"] [(df["score"] >= 5) & (df["score"] < 6)]
	five = funf.count()
	over_five = df["score"] [df["score"] >= 5]
	higher = over_five.count()
	neg_null = df["score"] [(df["score"] <= 0) & (df["score"] > -1)]
	neg_dec = neg_null.count()
	neg_eins = df["score"] [(df["score"] <= -1) & (df["score"] > -2)]
	neg_one = neg_eins.count()
	neg_zwei = df["score"] [(df["score"] <= -2) & (df["score"] > -3)]
	neg_two = neg_zwei.count()
	neg_drei = df["score"] [(df["score"] <= -3) & (df["score"] > -4)]
	neg_three = neg_drei.count()
	neg_vier = df["score"] [(df["score"] <= -4) & (df["score"] > -5)]
	neg_four = neg_vier.count()
	neg_funf = df["score"] [(df["score"] <= -5) & (df["score"] > -6)]
	neg_five = neg_funf.count()
	under_neg_five = df["score"] [df["score"] <= -6]
	neg_higher = under_neg_five.count()
	count = df[df.columns[0]].count()
	counts = [{"6 or higher counts": higher, "5 : 6 counts": five, "4 : 5 counts": four, "3 : 4 counts": three, "2 : 3 counts": two, "1 : 2 counts": one, "0 : 1 counts": decimals, "0 : -1 counts": neg_dec, "-1 : -2 counts": neg_one, "-2 : -3 counts": neg_two, "-3 : -4 counts": neg_three, "-4 : -5 counts": neg_four, "-5 : -6 counts": neg_five, "-6 or lower counts": neg_higher}]

	out_df = pd.DataFrame(counts)

	out_df.to_csv(args.stats_out)

import argparse
import gzip
import json
import csv
import pandas as pd
import math

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("embed_in", help = "gz.jsonl with verb frequencies")
	parser.add_argument("stats_out", help = "csv with statistics on frequency")

	args = parser.parse_args()

	with gzip.open(args.embed_in, "rt") as e_in:
		loaded_json = [{"score": json.loads(line)["score"]} for line in e_in]
		df = pd.DataFrame(loaded_json)
#	df = pd.read_json(args.verbs_in, lines=True, compression="gzip")

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
		counts = [{"6 or higher": higher, "5 : 6": five, "4 : 5": four, "3 : 4": three, "2 : 3": two, "1 : 2": one, "0 : 1": decimals, "0 : -1": neg_dec, "-1 : -2": neg_one, "-2 : -3": neg_two, "-3 : -4": neg_three, "-4 : -5": neg_four, "-5 : -6": neg_five, "-6 or lower": neg_higher}]

		out_df = pd.DataFrame(counts, index=["counts"])
		out_df_2 = out_df.apply(lambda row: row/count * 100, axis=1, result_type="expand")
		out_df_2.index = ["percent"]
		print(out_df_2)
		print(pd.concat([out_df, out_df_2]))

		pd.concat([out_df,out_df_2]).to_csv(args.stats_out)

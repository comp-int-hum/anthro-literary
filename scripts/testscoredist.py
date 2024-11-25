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

	with gzip.open(args.verbs_in, "rt") as v_in:
		for line in v_in:
			jline = json.loads(line)
#			print("jline loaded")
			df = pd.DataFrame([jline])
			df["score"] = pd.to_numeric(df["score"], errors="coerce")
			null = df["score"] [(df["score"] >= 0) & (df["score"] < 1)]
			decimals = null.count()
			eins = df["score"] [(df["score"] >= 1) & (df["score"] < 2)]
			one = eins.count()
#			one = df["score"].between(1, 2, inclusive="left").value_counts()
#			print(one)
#			one = df["score"].between(1, 2, inclusive="left").count()
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
			dec_ratio = str(decimals/count * 100) + "%"
			one_ratio = str(one/count * 100) + "%"
			two_ratio = str(two/count * 100) + "%"
			three_ratio = str(three/count * 100) + "%"
			four_ratio = str(four/count * 100) + "%"
			five_ratio = str(five/count * 100) + "%"
			higher_ratio = str(higher/count * 100) + "%"
			neg_dec_ratio = str(neg_dec/count * 100) + "%"
			neg_one_ratio = str(neg_one/count * 100) + "%"
			neg_two_ratio = str(neg_two/count * 100) + "%"
			neg_three_ratio = str(neg_three/count * 100) + "%"
			neg_four_ratio = str(neg_four/count * 100) + "%"
			neg_five_ratio = str(neg_five/count * 100) + "%"
			neg_higher_ratio = str(neg_higher/count * 100) + "%"
			percents = [{"6 or higher percentage": higher_ratio, "5 : 6 percentage": five_ratio, "4 : 5 percentage": four_ratio, "3 : 4 percentage": three_ratio, "2 : 3 percentage": two_ratio, "1 : 2 percentage": one_ratio, "0 : 1 percentage": dec_ratio, "0 : -1 percentage": neg_dec_ratio, "-1 : -2 percentage": neg_one_ratio, "-2 : -3 percentage": neg_two_ratio, "-3 : -4 percentage": neg_three_ratio, "-4 : -5 percentage": neg_four_ratio, "-5 : -6 percentage": neg_five_ratio, "less than -6 percentage": neg_higher_ratio}]
#			counts = [{"6 or higher counts": higher, "5 : 6 counts": five, "4 : 5 counts": four, "3 : 4 counts": three, "2 : 3 counts": two, "1 : 2 counts": one, "0 : 1 counts": decimals, "0 : -1 counts": neg_dec, "-1 : -2 counts": neg_one, "-2 : -3 counts": neg_two, "-3 : -4 counts": neg_three, "-4 : -5 counts": neg_four, "-5 : -6 counts": neg_five, "-6 or lower counts": neg_higher}]
#			stats = [{"percentages": percents, "counts": counts}]

#			out_df = pd.DataFrame(stats)
#			out_df = pd.DataFrame(percents, counts)
			out_df = pd.DataFrame(percents)

			out_df.to_csv(args.stats_out)

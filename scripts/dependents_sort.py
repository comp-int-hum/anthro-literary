import argparse
import csv
import pandas as pd

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("dependents_in", help = "gz.jsonl with verb frequencies and dependent verbs")
	parser.add_argument("sorted_out", help = "csv sorted by dependent verbs")

	args = parser.parse_args()

	df = pd.read_csv(args.dependents_in)

	df.sort_values(by=["dependents", "score"], ascending=[True, True], inplace=True)

	df.to_csv(args.sorted_out)

import argparse
import gzip
import json
import pandas as pd
import spacy
import codecs

nlp= spacy.load("en_core_web_sm")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help = "csv ")
	parser.add_argument("sorted_out", help = "csv containing verbs sorted by author")

	args = parser.parse_args()

	with codecs.open(args.verbs_in, "r", encoding="ISO-8859-1") as out_sorted:
		df = pd.read_json(out_sorted, lines=True)

		count = doc["verbs"].count_by()
		if df["score"] >=1:
			for token in doc["verbs"]:
				if count >1:
					df.groupby("verbs")
					df.sort_values("verbs", ascending=False)
					author_sort = df.groupby("author")["verbs"]
					author_sort.to_csv(args.sorted_out)

import argparse
import gzip
import json
import csv
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help = "gz.jsonl with verb frequencies")
	parser.add_argument("lemma_out", help = "csv with lemma frequencies")

	args = parser.parse_args()
	lemmatizer = nltk.WordNetLemmatizer()

	with gzip.open(args.verbs_in, "rt") as v_in, open(args.lemma_out, "wt", newline="") as l_out:
		out_writer = csv.writer(l_out)
		out_writer.writerow(["title", "author", "id", "sentence", "masked", "word", "score", "lemmas"])
		for line in v_in:
			jline = json.loads(line)
			print(jline["verbs"])
			lemmas = lemmatizer.lemmatize(jline["verbs"].lower(), pos = "v")
			print(lemmas)
			out_writer.writerow([jline["title"], jline["author"], jline["id"], jline["sentence"], jline["masked"], jline["word"], jline["score"], lemmas])

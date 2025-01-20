import argparse
import gzip
import json
import csv
import spacy

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help = "gz.jsonl with verb frequencies")
	parser.add_argument("lemmas_out", help = "csv with lemma frequencies")

	args = parser.parse_args()
	nlp = spacy.load("en_core_web_sm")

	with gzip.open(args.verbs_in, "rt") as v_in, open(args.lemmas_out, "wt", newline="") as l_out:
		out_writer = csv.writer(l_out)
		out_writer.writerow(["title", "author", "id", "sentence", "masked", "word", "score", "lemmas"])
		for line in v_in:
			jline = json.loads(line)
			doc = nlp(jline["verbs"])
			for token in doc:
				lemmas = token.lemma_
				out_writer.writerow([jline["title"], jline["author"], jline["id"], jline["sentence"], jline["masked"], jline["word"], jline["score"], lemmas])


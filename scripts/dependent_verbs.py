import argparse
import gzip
import json
import csv
import spacy

#this script is for supervised not self-supervised embeddings

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help="gz.jsonl with nouns and verbs")
	parser.add_argument("dependencies_out", help="csv with nouns and matching dependent verbs")

	args = parser.parse_args()
	nlp = spacy.load("en_core_web_sm")

	with gzip.open(args.verbs_in, "rt") as v_in, open(args.dependencies_out, "wt", newline="") as d_out:
		out_writer = csv.writer(d_out)
		out_writer.writerow(["title", "author", "id", "sentence", "masked", "word", "score", "verbs"])
		for line in v_in:
			jline = json.loads(line)
			doc1 = nlp(jline["sentence"])
			doc2 = nlp(jline["word"])
#			for token in doc["sentence"]:
#				if token == token in doc["word"]:
			for token in doc1:
				if token == token in doc2:
					dependents = token.head.text
					out_writer.writerow([jline["title"], jline["author"], jline["id"], jline["sentence"], jline["masked"], jline["word"], jline["score"], dependents])
#			for token in doc["word"]:
#				if token.head.pos_ in doc["sentence"]:
					#write token.head.text
				#if token.head.pos_ == VERB

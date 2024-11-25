import argparse
import gzip
import json
import csv
import spacy

nlp = spacy.load("en_core_web_sm")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help="gz.jsonl with nouns and verbs")
	parser.add_argument("dependencies_out", help="csv with nouns and matching dependent verbs")

	args = parser.parse_args()

	with gzip.open(args.verbs_in, "rt") as v_in, open(args.dependencies_out, "wt", newline="") as d_out:
		out_writer = csv.writer(d_out)
		out_writer.writerow(["title", "author", "id", "sentence", "masked", "word", "score", "verbs", "dependents"])
		for line in v_in:
			jline = json.loads(line)
#			print("loaded jline")
			doc = nlp(jline["masked"][0])
#			print("loaded doc")
			for token in doc:
#				print(token)
				if token.text == "mask":
#					print("target word found")
					print(token.text)
					for child in token.children:
						print(child)
						if child.pos_ == "VERB":
							print(child)
#							input()
							dependents = child.text
							out_writer.writerow([jline["title"], jline["author"], jline["id"], jline["sentence"], jline["masked"], jline["word"], jline["score"], jline["verbs"], dependents])

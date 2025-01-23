import argparse
import gzip
import json
import csv
import spacy

nlp = spacy.load("en_core_web_sm")

#this should run on embeddings sentences not verbs?

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("embed_in", help="gz.jsonl with embeddings")
	parser.add_argument("target_words", help="text file with target words")
	parser.add_argument("dependencies_out", help="csv with nouns and matching dependent verbs")

	args = parser.parse_args()

	with gzip.open(args.embed_in, "rt") as e_in, open(args.target_words, "r") as t_w, open(args.dependencies_out, "wt", newline="") as d_out:
		out_writer = csv.writer(d_out)
#		out_writer.writerow(["title", "author", "id", "sentence", "masked", "word", "score", "verbs", "dependents"])
		for line in e_in:
			jline = json.loads(line)
			doc = nlp(jline["sentence"])
#			root = [token for token in doc if token.dep_ == "ROOT"][0]
#			verbs = [child.text for child in root.children if child.pos_ == "VERB"]
			for sent in doc.sents:
				for w in t_w:
					for token in sent:
						if token.text == w:
							target = token
							head_one = target.head
							if head_one.pos_ == "VERB":
								print("target verb found first")
#								dependents = head_one.text
								#write out with "dependents": head_one.text
							else:
								head_two = head_one.head
								if head_two.pos_ == "VERB":
									print("target verb found second")
#									dependents = head_two.text
									#write out with "dependents": head_two.text
								else:
									print("nothing found")
									#write out with "dependents": "nothing found"

#					out_writer.writerow([jline["title"], jline["author"], jline["id"], jline["sentence"], jline["masked"], jline["word"], jline["score"], jline["verbs"], dependents])

#should be gz.jsonl instead of csv?

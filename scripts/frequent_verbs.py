import argparse
import gzip
import json
import spacy
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("embeddings_in", help = "masked sentences from embeddings gz.jsonl")
	parser.add_argument("verbs_out", help = "gz.jsonl with verbs and frequency")

	args, other = parser.parse_known_args()
	print("spacy has loaded")

	with gzip.open(args.embeddings_in, "rt") as in_embed, gzip.open(args.verbs_out, "wt") as v_out:
		for line in in_embed:
			jline = json.loads(line)
			print(jline)
			verbs = defaultdict(int)
			doc = nlp(jline["masked"])
			for token in doc:
				if token.pos_ == {"VERB"}:
					print(token.pos_)
					verbs[token.text]
					v_out.write(json.dumps(jline | {"verbs": verbs}) + "\n")

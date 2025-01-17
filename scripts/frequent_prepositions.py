import argparse
import gzip
import json
import spacy

nlp = spacy.load("en_core_web_sm")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("embeddings_in", help = "masked sentences from embeddings gz.jsonl")
	parser.add_argument("preps_out", help = "gz.jsonl with prepositions and frequency")

	args, other = parser.parse_known_args()
	print("spacy has loaded")

	with gzip.open(args.embeddings_in, "rt") as in_embed, gzip.open(args.preps_out, "wt") as p_out:
		for line in in_embed:
			jline = json.loads(line)
			doc = nlp(jline["masked"][0])
			for token in doc:
				print(token.pos_)
				if token.pos_ == "ADP":
					preposition = token.text
					print(preposition)
					p_out.write(json.dumps({"title": jline["title"], "author": jline["author"], "id": jline["id"], "sentence": jline["sentence"], "masked": jline["masked"], "word": jline["word"], "score": jline["score"], "prepositions": preposition}) + "\n")

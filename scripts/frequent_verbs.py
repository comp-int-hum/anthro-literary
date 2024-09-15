import argparse
import gzip
import json
import spacy

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
#			print(jline["score"])
#			print([key for key in jline.keys()])
#			input()
			doc = nlp(jline["masked"][0])
#			print(doc)
			for token in doc:
				print(token.pos_)
				if token.pos_ == "VERB":
#					print(token.pos_)
#					print(token.text)
#					input()
					token.text
					print(token.text)
					v_out.write(json.dumps({"title": jline["title"], "author": jline["author"], "id": jline["id"], "sentence": jline["sentence"], "masked": jline["masked"], "word": jline["word"], "score": jline["score"], "verbs": token.text}) + "\n")

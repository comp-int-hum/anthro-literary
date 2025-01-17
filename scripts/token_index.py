import argparse
import gzip
import json
import spacy

nlp = spacy.load("en_core_web_sm")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("embeddings_in", help = "masked sentences from embeddings gz.jsonl")
	parser.add_argument("indexed_out", help = "gz.jsonl with masked token indices")

	args, other = parser.parse_known_args()
	print("spacy has loaded")

	with gzip.open(args.embeddings_in, "rt") as in_embed, gzip.open(args.indexed_out, "wt") as i_out:
		for line in in_embed:
			jline = json.loads(line)
			doc = nlp(jline["masked"][0])
			for token in doc:
				print(token.text)
				if token.text == "[":
					mask_index = token.i
					print(token.i)
				elif token.text == "<":
					mask_index = token.i
				i_out.write(json.dumps({"title": jline["title"], "author": jline["author"], "id": jline["id"], "sentence": jline["sentence"], "masked": jline["masked"], "word": jline["word"], "score": jline["score"], "index": mask_index}) + "\n")

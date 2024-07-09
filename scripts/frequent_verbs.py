import gzip
import json
import spacy
import csv

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("embeddings_in", help = "masked sentences from embeddings gz.jsonl")
	parser.add_argument("verbs_out", help = "csv with verbs by frequency")

	args, other = parser.parse_known_args()
	nlp = spacy.load("en_core_web_sm")

	with gzip.open(args.embeddings_in, "rt") as in_embed, open(args.verbs_out, "wt", newline="") as v_out:
		out_writer=csv.writer(v_out)
		out_writer.writerow()
		doc = nlp(in_embed)
		verb_counts = doc.count_by(POS)
		for token in doc:
			if token.pos_ = {"VERB"}:
				for count in verb_counts.items:
					out_writer.writerow(token.pos_, count)

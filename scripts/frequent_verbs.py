import gzip
import json
import spacy

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("embeddings_in", help = "masked sentences from embeddings gz.jsonl")
	parser.add_argument("verbs_out", help = "gz.jsonl with verbs and frequency")

	args, other = parser.parse_known_args()
	nlp = spacy.load("en_core_web_sm")

	with gzip.open(args.embeddings_in, "rt") as in_embed, gzip.open(args.verbs_out, "wt") as v_out:
		doc = nlp(in_embed)
		for token in doc:
			if token.pos_ == {"VERB"}:
			verb_count = doc.count_by(POS)
				if count in verb_count.items > 1:
					v_out.write(json.dumps({ID: ["id"], Title: ["title"], Author: ["author"], Sentence: sent, Mask: masked_sentence, Word: w, Score: a_score.item(), Verb: token.pos_, Frequency: count})+"n")
					#omit sent to only include masked sent?

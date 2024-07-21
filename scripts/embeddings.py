import argparse
import gzip
import json
import logging
from transformers import AutoTokenizer, BertForMaskedLM, RobertaForMaskedLM
from torch.nn.functional import softmax
import re
import torch

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("samples_in", help="tokenized gz.jsonl file containing fulltext and metadata")
	parser.add_argument("embeddings_out", help="gz.jsonl file with embeddings and texts")
	parser.add_argument("--model", help="bert or roberta model name")
	parser.add_argument("--target_words", nargs="+", help="Embed all sents containing these words. Case insensitive")
	parser.add_argument("--animate_pronouns", nargs="+", help="list of animate pronouns")
	parser.add_argument("--inanimate_pronouns", nargs="+", help="list of inanimate pronouns")

	args, other = parser.parse_known_args()
	a_t = AutoTokenizer.from_pretrained(args.model)
	if args.model == "bert-base-uncased":
		model = BertForMaskedLM.from_pretrained(args.model)
	elif args.model == "FacebookAI/roberta-base":
		model = RobertaForMaskedLM.from_pretrained(args.model)
	else:
		exit

#	print(args.target_words)
	search_pattern = re.compile(r"\b(?:%s)\b" % "|".join(args.target_words), re.IGNORECASE)
	inputs_animate = a_t(" ".join(args.animate_pronouns), return_tensors = "pt", add_special_tokens=False).input_ids
	inputs_inanimate = a_t(" ".join(args.inanimate_pronouns), return_tensors = "pt", add_special_tokens=False).input_ids

	with gzip.open(args.samples_in, "rt") as in_s, gzip.open(args.embeddings_out, "wt") as e_out:
		n=0
		for line in in_s:
			if n<1000000000:
				sent_embeds = []
				j_line = json.loads(line)
				for sent in j_line["full_text"]:
					if re.search(search_pattern, sent):
						for w in args.target_words:
							masked_sentence = re.subn(r"\b(?:%s)\b" % w, a_t.mask_token, sent, re.IGNORECASE)
							if masked_sentence[1] > 0:
#								print(masked_sentence[0])
								try:
									tokenized_sent = a_t(masked_sentence[0], return_tensors="pt")
									with torch.no_grad():
										logits = model(**tokenized_sent).logits
									mask_token_index = (tokenized_sent.input_ids == a_t.mask_token_id)[0].nonzero(as_tuple=True)[0]
									masked_token_logits = logits[0, mask_token_index]
									print(masked_token_logits.shape)
									pdf = softmax(masked_token_logits, dim=-1)
									a_score = torch.log(torch.sum(pdf[0, inputs_animate]))-torch.log(torch.sum(pdf[0, inputs_inanimate])).item()
									print(a_score)
									e_out.write(json.dumps(j_line | {"masked": masked_sentence, "word": w, "score": a_score.values()}))
								except RuntimeError:
									e_out.write(json.dumps(j_line | {"masked": masked_sentence, "word": w, "score": "error"}))
			n=n+1

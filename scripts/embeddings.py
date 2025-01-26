import argparse
import gzip
import json
import logging
from transformers import AutoTokenizer, BertForMaskedLM, RobertaForMaskedLM
from torch.nn.functional import softmax
import re
import torch
import spacy
import numpy as np
import scipy

if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", help="tokenized gz.jsonl file containing fulltext and metadata")
        parser.add_argument("--outputs", help="gz.jsonl file with embeddings and texts")
        parser.add_argument("--model", help="bert or roberta model name")
        parser.add_argument("--dep_include", nargs="+", default=["nsubj", "dobj"], help="use only these noun dependency relations")
        parser.add_argument("--target_words", help="Embed all sents containing these words. Case insensitive")
        parser.add_argument("--animate_pronouns", nargs="+", help="list of animate pronouns")
        parser.add_argument("--inanimate_pronouns", nargs="+", help="list of inanimate pronouns")
        parser.add_argument("--all_nouns", action="store_true", default=False, help="if true, forget --target_words and evaluate all nouns in the parse")
        parser.add_argument("--device", default="cpu")

        args, other = parser.parse_known_args()
        nlp = spacy.load("en_core_web_sm")
        a_t = AutoTokenizer.from_pretrained(args.model)
        if args.model == "bert-base-uncased":
                model = BertForMaskedLM.from_pretrained(args.model).to(args.device)
        elif args.model == "bert-base-cased":
                model = BertForMaskedLM.from_pretrained(args.model).to(args.device)
        elif args.model == "roberta-base":
                model = RobertaForMaskedLM.from_pretrained(args.model).to(args.device)

        if not args.all_nouns:
                with open(args.target_words) as tw:
                        t_w = [t.strip() for t in tw.readlines()]
                print(f"Target words: {t_w}")
                search_pattern = re.compile(r"\b(?:%s)\b" % "|".join(t_w), re.IGNORECASE)
                

        print(f"Animate words: {args.animate_pronouns}")
        print(f"Inanimate words: {args.inanimate_pronouns}")
        inputs_animate = [a_t.get_vocab()[x] for x in args.animate_pronouns]
        inputs_inanimate = [a_t.get_vocab()[x] for x in args.inanimate_pronouns]
        print(inputs_animate)
        print(inputs_inanimate)

        def get_as(masked_sentence):
                print(masked_sentence)
                token_ids = a_t.encode(masked_sentence, return_tensors="pt").to(args.device)
                masked_position = (token_ids.squeeze() == a_t.mask_token_id).nonzero()
                try:
                        masked_pos = [mask.item() for mask in masked_position][0]
                except IndexError:
                        temp = a_t.encode(masked_sentence, return_tensors="pt").to(args.device)
                        masked_position = (temp.squeeze() == a_t.mask_token_id).nonzero()
                        try:
                                if (int(masked_position[0] + 256)) > len(temp[0]):
                                        token_ids = torch.reshape(temp[0][-512:], (1, 512))
                                else:
                                        token_ids = torch.reshape(temp[0][masked_position[0] - 256:masked_position[0]+256], (1, 512))
                        except IndexError:
                                return np.array([0])
                        masked_position = (token_ids.squeeze() == a_t.mask_token_id).nonzero()
                        masked_pos = [mask.item() for mask in masked_position ][0]
                with torch.no_grad():
                        out = model(token_ids)
                
                last_hidden = out.logits.squeeze()
                masked_token_logits = last_hidden[masked_pos].cpu().numpy()
                pdf = scipy.special.softmax(masked_token_logits)
                a_score = np.log(np.sum([pdf[i] for i in inputs_animate])) - np.log(np.sum([pdf[i] for i in inputs_inanimate])) 
                return a_score
                
        n_sent = 0
        with gzip.open(args.input, "rt") as in_s, gzip.open(args.outputs, "wt") as e_out:
                for line in (in_s):
                        sent_embeds = []
                        j_line = json.loads(line)
                        for sent in j_line["full_text"]:
                                doc = nlp(sent)
                                for parsed_sent in doc.sents:
                                        for noun_chunk in parsed_sent.noun_chunks:
                                                if not args.all_nouns:
                                                        if re.findall(search_pattern, noun_chunk.text) and noun_chunk.root.dep_ in args.dep_include:
                                                                verb = noun_chunk.root.head.lemma_.lower()
                                                                for w in t_w:
                                                                        if w.lower() in noun_chunk.text.lower():
                                                                                n_sent +=1
                                                                                masked_sentence = re.subn(r"\b(?:%s)\b" % re.escape(noun_chunk.text), a_t.mask_token, parsed_sent.text, re.IGNORECASE)
                                                                                a_score = get_as(masked_sentence[0].strip())
                                                                                e_out.write(json.dumps(j_line | {"sentence": parsed_sent.text, "masked": masked_sentence, "word": w,
                                                                                                                 "score": a_score.item(), "verb": verb, "np": noun_chunk.text}) + "\n")
                                                else:
                                                        if noun_chunk.root.dep_ in args.dep_include:
                                                                n_sent += 1
                                                                verb = noun_chunk.root.head.lemma_.lower()
                                                                masked_sentence = re.subn(r"\b(?:%s)\b" % re.escape(noun_chunk.text), a_t.mask_token, parsed_sent.text, re.IGNORECASE)
                                                                a_score = get_as(masked_sentence[0])
                                                                e_out.write(json.dumps(j_line | {"sentence": parsed_sent.text, "masked": masked_sentence, "word": noun_chunk.root.text.lower(),
                                                                                         "score": a_score.item(), "verb": verb, "np": noun_chunk.text}) + "\n")
                                                        
        print(f"Found {n_sent} sents")                                                                         
                                                

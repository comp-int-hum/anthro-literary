import argparse
import json
import re
import gzip

if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("corpus", help = "json containing corpus and metadata")
	parser.add_argument("sentences", help = "json containing sentences with metadata")
	args = parser.parse_args()

	with open(args.corpus, "rt") as corpus_in, gzip.open(args.sentences, "wt") as corpus_out:

		for line in corpus_in:
			try:
				jl = json.loads(line)
				jl["full_text"] = []
#				print([key for key in jl.keys()])
#				print(jl["segments"])
#				print(list(jl.values()))
				for segment in jl["segments"].values():
#					print(segment)
					for segment_text in segment:
						sents = re.split(r" *[\.\?!][\'\"\)\]]* *", segment_text)
#						print(sents)
						jl["full_text"] += sents
#						print(jl["full_text"])
				corpus_out.write(json.dumps(jl)+"\n")
			except:
				pass

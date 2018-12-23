import morph_config as mc
from nltk.tokenize import word_tokenize

def suffix_code(s):
	for suffix in mc.suffix_table:
		if len(s) <= len(suffix): continue
		if s[-1*len(suffix):] == suffix: return suffix
	return None

def contribution(count):
	return count / (2 ** count)

count_table = {}

for suffix in mc.suffix_table:
	count_table[suffix] = {}

with open(mc.file_name, 'r', encoding = 'utf-8') as lines:
	idx = 0
	for line in lines:
		line = line.lower()
		tokens = word_tokenize(line)
		for token in tokens:
			idx += 1
			suffix = suffix_code(token)
			if suffix in mc.suffix_table:
				if token in count_table[suffix]:
					count_table[suffix][token] += 1
					count_table[suffix]["__TOTAL__"] += 1
				else:
					count_table[suffix][token] = 1
					count_table[suffix]["__TOTAL__"] = 1

for suffix in mc.suffix_table:
	P = 0
	P2 = 0
	for key, val in count_table[suffix].items():
		if key == "__TOTAL__": continue
		if val == 1 : P2 += 1
		P += contribution(val)
	P2 /= count_table[suffix]["__TOTAL__"]
	print("%s : %f" % (suffix, P))
	print("%s : %f" % (suffix, P2))

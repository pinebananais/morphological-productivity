import morph_config as mc
from nltk.tokenize import word_tokenize
import sys

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def suffix_code(s):
	for suffix in mc.suffix_table:
		if len(s) <= len(suffix): continue
		if s[-1*len(suffix):] == suffix: return suffix
	return None

def contribution(count):
	return count / (2 ** count)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

count_table = {}

for suffix in mc.suffix_table:
	count_table[suffix] = {}

total_idx = sum(1 for line in open(mc.file_name, encoding = 'utf-8'))
word_cnt = 0
with open(mc.file_name, 'r', encoding = 'utf-8') as lines:
	idx = 0
	for line in lines:
		idx += 1
		if idx % 1000 == 0: printProgress(idx, total_idx, 'Progress:', 'Complete', 1, 50)
		line = line.lower()
		tokens = word_tokenize(line)
		for token in tokens:
			word_cnt += 1
			suffix = suffix_code(token)
			if suffix in mc.suffix_table:
				if token in count_table[suffix]:
					count_table[suffix][token] += 1
					count_table[suffix]["__TOTAL__"] += 1
				else:
					count_table[suffix][token] = 1
					count_table[suffix]["__TOTAL__"] = 1

col_len = 12
if mc.flag_1: col_len += 12
if mc.flag_2: col_len += 12

print("")
print("Total %d words in dataset." % word_cnt)
for i in range(col_len):
	print("=", end="")
print("")
print("|   suffix   |", end="")
if mc.flag_1: print("  method1 |", end="")
if mc.flag_2: print("  method2 |", end="")
print("")
for i in range(col_len):
	print("=", end="")
print("")
for suffix in mc.suffix_table:
	P1 = 0
	P2 = 0
	for key, val in count_table[suffix].items():
		if key == "__TOTAL__": continue
		if val == 1 : P2 += 1
		P1 += contribution(val)
	P2 /= count_table[suffix]["__TOTAL__"]
	print("|-%-11s|" % suffix, end="")
	if mc.flag_1: print("%10.2f|" % P2, end="")
	if mc.flag_2: print("%10.2f|" % P1, end="")
	print("")
for i in range(col_len):
	print("=", end="")
print("")

import sys


def output(sents, begin, end, outfile, user):
    annotator = user
    sql = "insert into dependancy(sentid,sent,dep_sent,annoter) values"
    i = begin
    raw_sent = ' '.join(['[' + str(id) + ']' + tok[0] + '/' + tok[1] for id, tok in enumerate(sents[begin])])
    sql += "('" + str(i) + "','" + raw_sent + "','"
    rels = "\t\t".join(
        ['[' + str(tok[2]) + ']' + sents[begin][tok[2]][0] + '_[' + str(id + 1) + ']' + tok[0] + '(' + tok[3] + ')' for
         id, tok in enumerate(sents[begin][1:])])
    sql += rels + "','" + annotator + "')"
    i += 1
    for sent in sents[begin + 1:end + 1]:
        raw_sent = ' '.join(['[' + str(id) + ']' + tok[0] + '/' + tok[1] for id, tok in enumerate(sent)])
        sql += ",('" + str(i) + "','" + raw_sent + "','"
        rels = "\t\t".join(
            ['[' + str(tok[2]) + ']' + sent[tok[2]][0] + '_[' + str(id + 1) + ']' + tok[0] + '(' + tok[3] + ')' for
             id, tok in enumerate(sent[1:])])
        sql += rels + "','" + annotator + "')"
        i += 1
    fo = open(outfile, "w")
    fo.write(sql)


if __name__ == "__main__":
    fi = open("./corpus", "r")
    fi = fi.read()
    sents = fi.strip().split("\n\n")
    print
    "total sents: ", len(sents)
    sentences = []
    n = 0
    for sent in sents:
        sentences.append([])
        sentences[n].append(("Root", "Root", -1, "-NULL-"))
        lines = sent.strip().split("\n")
        for line in lines:
            items = line.strip().split("\t")
            sentences[n].append((items[1], items[3], int(items[6]), items[7]))
        n += 1
    for i in range(10):
        output(sentences, i * 100, i * 100 + 99,
               "huawei" + str(i * 100) + "-" + str(i * 100 + 99) + "-user" + str(i) + ".sql", "user" + str(i))
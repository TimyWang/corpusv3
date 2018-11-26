def output(outfile, sents):
    fo = open(outfile, "w")
    for sent in sents:
        for idx, tok in enumerate(sent):
            line = str(idx + 1) + "\t" + tok["tok"] + "\t" + tok["tok"] + "\t" + tok["pos"] + "\t" + tok["pos"] + "\t_\t" + str(tok["hed"]) + "\t" + tok["rel"] + "\t_\t_\n"
            fo.write(line)
        fo.write("\n")


def process(infos):
    sents = []
    # fo =open("G:\corpus\dependancy_test.txt", "w")
    for info in infos:
        # sent = [{"tok": token[0], "pos": token[1]} for token in
        #         [tok.split("]")[1].split("/") for tok in info["tokens"]]]
        sent=[]
        for tok in info["tokens"]:
            token = tok.split("]")[1].split("/")
            # if len(token)==2:
            if token[0] =="Root":
                pass
            else:
                sent.append({"tok": token[0], "pos": token[1]})
        for rel in info["origin"]:
            items = rel.split("_")
            # print(items)
            # [3]很_[1]他(Exp)		[6]很_[2]他(Exp)		[3]很_[3]很(mDegr)
            index = int(items[1].split("]")[0].strip("["))   #index为 每行第 index个词的位置
            head = int(items[0].split("]")[0].strip("["))
            relation = items[1].split("(")[1].strip(")")
            # print(index, head, relation)
            sent[index-1]["hed"] = head    #第一个是root
            sent[index-1]["rel"] = relation
        sents.append(sent)
    print(sents[0])
    return sents


if __name__ == "__main__":
    fi = open("G:\corpus\dependancy.csv", "r", encoding='utf')
    fo =open("G:\corpus\dependancy_test.txt", "w")
    fi = fi.read()
    sents = fi.strip().split("\n")
    infos = []
    for sent in sents:
        info = {}
        items = [it.strip("\"") for it in sent.strip().split(";")]
        # sentid	sent	dep_sent	res_sent	tag 	annoter 	time	skip	comment
        if items[7] == "1": continue  # skip the skipped sents
        info["tokens"] = items[1].strip().split()
        info["origin"] = items[2].strip().split("\t\t")
        info["result"] = items[3].strip().split("\t")
        infos.append(info)
        # fo.write(str(info["tokens"])+";"+str(info["origin"])+";"+str(info["result"])+"\n")
    sents = process(infos)
    print(len(sents))
    for sent in sents:
        for i in range(len(sent)):
            fo.write(str(sent[i]["hed"])+"\n"+str(sent[i]))
        # fo.write(str(sent)+ "\n")
    output("G:\corpus\lannotated_test.conll", sents)

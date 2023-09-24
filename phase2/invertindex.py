# sourcery skip: assign-if-exp, ensure-file-closed, merge-else-if-into-elif, swap-if-else-branches
import heapq
from operator import index
import imports as im

if __name__ == "__main__":
    onlyfiles = list(im.os.listdir('/scratch/shivansh.s/temp'))
    # onlyfiles = list(im.os.listdir('./temp'))
    worddict = {}
    start = im.time.time()
    count = 0
    written = 0
    index_path = im.sys.argv[1]
    lwf = open(f'{index_path}lastword.txt', 'a')
    twf = open(f'{index_path}lasttitle.txt', 'w')
    im.ic(index_path)
    n = len(onlyfiles)
    fps = []
    pq = []
    for i in range(n):
        file = open(f'/scratch/shivansh.s/temp/{onlyfiles[i]}', 'r')
        # file = open(f'./temp/{onlyfiles[i]}', 'r')
        fps.append(file)
        line = file.readline().strip()
        word, docid, label = line.split()
        pq.append((word, docid, label, i))
    im.heapify(pq)
    prevword = None

    while pq:
        node = im.heappop(pq)
        count += 1
        word, docid, label, i = node
        if count >= im.HEAPSIZE and prevword != word:
            fpath = f'{index_path}{written}.txt'
            with open(fpath, 'w+') as f:
                for word, value in worddict.items():
                    docs = []
                    for v, k in value.items():
                        dstring = f'{v}'
                        count = 0
                        for l, lv in k.items():
                            if lv > 1:
                                dstring = f'{dstring}{l}{lv}'
                            else:
                                dstring = f'{dstring}{l}'
                            count += lv
                        docs.append((dstring, count))
                    fdocs = [d[0] for d in docs]
                    f.write(f"{word}{im.DOCS}{'*'.join(fdocs)}{im.INV}")
            lwf.write(f'{prevword} {written}\n')
            im.ic(prevword, written, im.time.time() - start)
            written += 1
            worddict = {}
            count = 0
        if word not in worddict:
            worddict[word] = {
                docid: {
                    label: 1
                }
            }
        else:
            if docid not in worddict[word]:
                worddict[word][docid] = {
                    label: 1
                }
            else:
                if label not in worddict[word][docid]:
                    worddict[word][docid][label] = 1
                else:
                    worddict[word][docid][label] = worddict[word][docid][label] + 1
        line = fps[i].readline().strip()
        if len(line) > 0:
            w, d, l = line.split()
            im.heappush(pq, (w, d, l, i))
        prevword = word
    lwf.close()
    titlefiles = list(im.os.listdir(f'{index_path}titles/'))
    titlefiles = im.natsorted(titlefiles)
    tcounts = [int(im.os.popen(f'tail -1 {index_path}titles/{titfile}').read().strip().split()[0]) for titfile in titlefiles]
    for tc in tcounts:
        twf.write(f'{tc}\n')
    twf.close()

import imports as im
from tqdm import tqdm

index_path = im.sys.argv[1]
invindexfiles = list(im.os.listdir(index_path))
invindexfiles = im.natsorted(invindexfiles)
titlefiles = list(im.os.listdir(f'{index_path}titles/'))
titlefiles = im.natsorted(titlefiles)
im.ic(titlefiles[-1], invindexfiles[-4])
numfiles = len(titlefiles) + len(invindexfiles) - 1
im.ic(numfiles)
invindexfiles = invindexfiles[:-3]
tokens = [int(im.os.popen(f'wc -l {index_path}{path}').read().strip().split()[0]) for path in tqdm(invindexfiles)]
im.ic(sum(tokens))


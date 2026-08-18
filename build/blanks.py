import json,sys
pages=json.load(open(sys.argv[1])); out=sys.argv[2]; total=int(sys.argv[3])
keys=['ch-bev','ch-hors','ch-bread','ch-bkfst','ch-soup','ch-salad','ch-meat','ch-poul','ch-fish','ch-cass','ch-veg','ch-sauce','ch-pie','ch-dess','ch-bars','ch-frost','ch-pres','ch-extra','people','index']
blanks=[]; off=0
for k in keys:
    p=pages[k]+off
    if p%2==0: blanks.append(k); off+=1
if (total+off)%2==1: blanks.append('end')
json.dump(blanks,open(out,'w')); print('blanks:',blanks)

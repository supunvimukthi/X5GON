# script to run in console to check output
f = open("Scripts/output1_tf_0.8_wiki_0.95_procs_10.txt","r")
results = eval(f.read())
res = [j for i in results for j in i]
max([i[1] for i in res])
[i[1] for i in res if i[3] != i[2]]

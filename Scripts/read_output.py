# script to run in console to check output
f = open("Scripts/output_tf_0.85_wiki_0.95_procs_10.txt","r")
results = eval(f.read())
res = [j for i in results for j in i]
max([i[1] for i in res])
[i for i in res if i[3] != i[2]]

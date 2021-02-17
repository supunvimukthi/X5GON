from firebase import firebase

bn=firebase.FirebaseApplication('https://slvseng-default-rtdb.firebaseio.com', None)
scores=bn.get('/Scores/-MQSmP8IdIBqxIf4rvxd/score',None)
bn.put('/Scores/-MQSmP8IdIBqxIf4rvxd','total',scores)
globals=bn.get('/FixtureUserScore/global',None)
for i in globals:
    globals[i]['total']=globals[i]['score']
bn.put('/FixtureUserScore','global',globals)

firebase = firebase.FirebaseApplication('https://lpltournament.firebaseio.com', None)
a = firebase.get('/FixtureUser', None)
c = firebase.get('/Fixtures/-MMAeHYbmiF5joAiGyJj/playing', None)
c = list(c.keys())

final={}
for i in a['round4']:
    k = a['round4'][i]
    boost = k['boost']
    bo = -1
    for i in range(len(boost)):
        if boost[i] and boost[i]['id'] == '-MMAeHYbmiF5joAiGyJj':
            bo = i
            boost[i] = False
    total = 0
    for j in range(len(k['team'])):
        for l in range(len(k['team'][j])):
            if k['team'][j][l]['id'] in c:
                if k['team'][j][l]['id'] == k['captain'] and bo == 0:
                    k['team'][j][l]['points'] -= 12
                    total += 12
                elif k['team'][j][l]['id'] == k['vicecaptain'] and bo == 0:
                    k['team'][j][l]['points'] -= 6
                    total += 6
                else:
                    k['team'][j][l]['points'] -= 4
                    total += 4
    k['score'] -= total
    s=boost[0]
    if s:
        s=boost[0]['id']
    final[k['user']] = total


from pycricbuzz import Cricbuzz
c = Cricbuzz()
import json
c = Cricbuzz()
matches = c.matches()
print (json.dumps(matches,indent=4)) #for pretty prinitng

def match_info(mid):
    c = Cricbuzz()
    minfo = c.matchinfo(mid)
    print(json.dumps(minfo, indent=4, sort_keys=True))

match_info("31978")

def live_score(mid):
    c = Cricbuzz()
    lscore = c.livescore(mid)
    print(json.dumps(lscore, indent=4, sort_keys=True))

live_score("31978")

def commentary(mid):
    c = Cricbuzz()
    comm = c.commentary(mid)
    print(json.dumps(comm, indent=4, sort_keys=True))

def scorecard(mid):
    c = Cricbuzz()
    scard = c.scorecard(mid)
    print(json.dumps(scard, indent=4, sort_keys=True))

live_score("31978")
commentary("31978")
scorecard("31978")
a=tten.get('/Fixtures/-MRoNm2QwjqRLaZcMfnw/playing',None)
match='-MRoNm2QwjqRLaZcMfnw'
b=tten.get('/FixtureUser/round2',None)
for i in b:
    ind=-1
    for k,j in enumerate(b[i]['boost']):
        if j and j['id']==match:
            ind=k
    score_chng=0
    for m in b[i]['team']:
        for n in m:
            # captain
            if n['id'] in a and ind==0:
                if b[i]['captain']==n['id']:
                    n['change'] = 3 * a[n['id']]['points']
                elif b[i]['vicecaptain']==n['id']:
                    n['change'] = 2 * a[n['id']]['points']
                else:
                    n['change'] = a[n['id']]['points']
            # boundaries
            elif n['id'] in a and ind==1:
                    n['change']=a[n['id']]['points']+a[n['id']]['fours']+2*a[n['id']]['sixes']
            # wickets
            elif n['id'] in a and ind == 1:
                n['change'] = a[n['id']]['points'] + 25*a[n['id']]['wickets']
            if 'change' in n:
                score_chng+=n['change']
    b[i]['score_change']=score_chng
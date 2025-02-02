import sys
sys.stdin = open("input.txt", "r")

n, m, k = map(int, input().split()) #격자 크기, 플레이어 수, 라운드 수
gun = [[[0] for _ in range(21)] for _ in range(21)] #총gun 맵
p = [[-1,-1] for _ in range(m)] #플레이어 위치
pd = [0 for i in range(m)] #플레이어 방향
dr = [-1,0,1,0]
dc = [0,1,0,-1]
ps = [0 for i in range(m)] #플레이어 초기능력치
pg = [0 for i in range(m)] #플레이어가 갖고있는 총의 세기
point = [0 for i in range(m)]

        
 
for i in range(n):
    li = list(map(int, input().split()))
    for j in range(len(li)):
        gun[i+1][j+1] = [li[j]]
for i in range(m): 
    x, y, d, s = map(int, input().split())
    p[i] = [x,y]
    pd[i] = d
    ps[i] = s


def rotate90(pid):
    pd[pid] = (pd[pid] + 1) % 4

def walk(pid): 
    nr,nc = p[pid][0]+dr[pd[pid]], p[pid][1]+dc[pd[pid]]
    #print(f"In Walk()... nr, nc={nr},{nc}")
    if 1<=nr<=n and 1<=nc<=n:
        p[pid][0], p[pid][1] = nr, nc
    else:
        #print("rotating")
        rotate90(pid)
        rotate90(pid)
        nr,nc = p[pid][0]+dr[pd[pid]], p[pid][1]+dc[pd[pid]]
        p[pid][0], p[pid][1] = nr, nc
        #print(nr, nc)

def exist_enemy(pid):
    for i in range(len(p)):
        if pid == i: continue
        enemy = p[i]
        if enemy == p[pid]:
            return i #enemy의 idx를 리턴
    return -1


#플레이어의 위치에 gun drop
def dropGun(pid):
    gx, gy = p[pid][0], p[pid][1]
    gun[gx][gy].append(pg[pid])
    #print(gun[gx][gy])
    #print(f"pid={pid} drops the gun {pg[pid]}")
    pg[pid]=0


#플레이어의 위치에 놓인 총들 중 max값 얻기
def getMaxGun(pid):
    gx, gy = p[pid][0], p[pid][1]
    grab = max(gun[gx][gy])

    gun[gx][gy].remove(grab)
    pg[pid] = grab
    #print(f"pid={pid} gets gun {grab}")
    #print(f"pg status = {pg}")

def fight(mi, ei): #me index, #enemy index
    #print(f"fight! {mi}<->{ei}")
    #print(f"mi power = {ps[mi] + pg[mi]}")
    #print(f"ei power = {ps[ei] + pg[ei]}")
    if ps[mi] + pg[mi] > ps[ei] + pg[ei]:
        return mi, ei
    elif ps[mi] + pg[mi] < ps[ei] + pg[ei]:
        return ei, mi
    else: 
    #초기+총 합이 둘이 같다면
    #초기 능력치가 높은 플레이어 승
        if ps[mi] > ps[ei]:
            return mi, ei
        else:
            return ei, mi
    
def loserWalk(pid):
    #print(f"loser {pid} walking")
    while True:
        nr,nc = p[pid][0]+dr[pd[pid]], p[pid][1]+dc[pd[pid]]
        #print(f"loser {pid} gonna go to [{nr},{nc}]")
        r, c = p[pid][0], p[pid][1]
        p[pid][0], p[pid][1] = nr,nc
        if 1<=nr<=n and 1<=nc<=n and exist_enemy(pid)==-1:
            #print(f"nr, nc, exist_enemy(pid) = {nr},{nc},{exist_enemy(pid)}")
            break
        else:
            p[pid][0], p[pid][1] = r,c
            rotate90(pid)


for _ in range(k):
    for pid in range(m):
        #print("##################pid=%d 차례" % pid)
        walk(pid)
        ei = exist_enemy(pid) #enemy 인덱스
        if ei != -1:
            #두 플레이어가 싸우게 됩니다
            win, lose = fight(pid, ei)

            #이긴 사람 포인트 획득 (각각의 ps+pg 합 차이)
            #print(f"winval={ps[win]+pg[win]},loseval={ps[lose]+pg[lose]}")
            #print(f"prev point={point}")
            point[win] += (ps[win]+pg[win])-(ps[lose]+pg[lose])
            #print(f"after point={point}")

            #진사람 총 내리고 전진
            dropGun(lose)
            loserWalk(lose)

            #이긴 사람 공격력 높은 총 얻기
            getMaxGun(win)
        else: 
            #print("no enemy exists")
            dropGun(pid)
            getMaxGun(pid)
        #print(p)
    
"""
#enemy 인덱스가 -1이라면
#총이 없는 경우, 세기가 0인 총을 갖고있는 것과 동일
#총 갖고있다 -> 버리고 제일 쎈거 갖는다
#총 안갖고있다 -> 0총 버리고 제일 쎈거 갖는다
#동일한 로직 적용 가능
"""
        
#for i in gun:
     #print(i)   
for i in point:
    print(i, end = ' ')
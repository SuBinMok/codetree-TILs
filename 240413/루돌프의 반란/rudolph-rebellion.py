#n:크기 m:게임 턴수 p: 산타수, c: 루돌프 힘 d: 산타 힘

from collections import deque
n, m, p, c, d = map(int, input().split())
rx, ry = map(int, input().split())
sixy = [list(map(int, input().split())) for _ in range(p)]
sr = [0]*p
game = [[-3]*n for _ in range(n)]
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
#게임판 초기화 : 루돌프 -9, 산타 0~p, -3 : 빈공간
#산타 기절 0, 탈락 -1, 살아있음 상태 1는 sixy[i][0]에서 알수 있음
rx = rx-1
ry = ry-1
for i in range(p):#산타 자리
    sixy[i][1] -=1
    sixy[i][2] -=1
    game[sixy[i][1]][sixy[i][2]] = i
    sixy[i][0]= 1


def boom(i, who):
    movx=0
    movy=0
    queue = deque()
    w = 0
    if who == 1:#루돌프가 충돌
        sr[i] += c
        w = c
    elif who == 2: #산타가 충돌
        sr[i] += d
        w = d
    #충돌 뒤 밀려날 방향 계산
    movx = (sixy[i][1] - rx)
    movy = (sixy[i][2] - ry)
    queue.append((sixy[i][1], sixy[i][2], movx, movy, w, i))
    while queue:
        bx, by, nx, ny, ww, s = queue.popleft()
        cx, cy = rx+nx*ww, ry+ny*ww # cx, cy 는 힘(w)만큼 밀려난 위치
        if 0<=cx<n and 0<=cy<n: #밀린 위치가 범위 내이면...
            if game[cx][cy] < -1 : #밀린 위치에 산타가 없으면
                game[bx][by] = -3
                game[cx][cy] = s #맵에 새 위치에 산타번호 표시
                sixy[s][1] = cx #위치 갱신
                sixy[s][2] = cy #위치 갱신
            elif game[cx][cy] >= -2 : #밀린 위치에 누군가 있으면 0~q: 일반산타
                #상호작용
                ns = game[cx][cy]
                queue.append((cx, cy, nx, ny, 1, ns))   
        else:
            sixy[s][0] = -3 #산타 탈락
            game[sixy[s][1]][sixy[s][2]] = -3
    if sixy[i][0] >= 0:#산타가 탈락이 아니면 기절 업데이트
        sixy[i][0] = -2

for mm in range(m): #m번 반복
    #루돌프 움직임
    min_distance = 9999999
    close_santa = 0
    for i in range(p): #루돌프와 산타 거리 계산
        esi, esx, esy = sixy[i][0], sixy[i][1], sixy[i][2]
        if esi >= -2: #기절 산타 포함 돌진 가능
            dis = (rx-esx)**2 + (ry-esy)**2
            if dis < min_distance:
                close_santa = i
                min_distance = dis
            elif dis == min_distance:
                if sixy[i][1] > sixy[close_santa][1]:
                    close_santa = i
                    min_distance = dis
                elif sixy[i][2] == sixy[close_santa][2]:
                    if sixy[i][2] > sixy[close_santa][2]:
                        close_santa = i
                        min_distance = dis
        else:
            continue
    rx = int((rx+sixy[close_santa][1])/2)
    ry = int((ry+sixy[close_santa][2])/2)
    #충돌 검사
    if rx == sixy[close_santa][1] and ry == sixy[close_santa][2]:
        boom(close_santa, 1) 
    #루돌프 위치 갱신
    

    #산타 움직임
    for i in range(p):
        close_ru = 999999
        close_ru_dir = -1
        tsx, tsy = 0, 0
        if sixy[i][0] ==-3:
            continue
        elif sixy[i][0] == 1: #산타가 생생한 상태
            for a in range(4):#4 방향으로 탐색 
                tsx = sixy[i][1] + dx[a]
                tsy = sixy[i][2] + dy[a]
                if 0>tsx or tsx>=n or 0>tsy or tsy>=n or game[tsx][tsy] > -3: 
                    #해당 위치가 범위에서 벗어나거나, 산타가 있는 경우
                    continue
                ru_dis = (rx-tsx)**2 + (ry-tsy)**2
                if ru_dis < close_ru:
                    close_ru = ru_dis
                    close_ru_dir = a
            nsx = sixy[i][1] + dx[close_ru_dir]
            nsy = sixy[i][2] + dy[close_ru_dir]
            if nsx == rx and nsy == ry:
                boom(i, 2) #산타가 움직여서 충돌난 경우 2
            else:
                game[sixy[i][1]][sixy[i][2]] = -3
                sixy[i][1]= nsx
                sixy[i][2] = nsy
                game[sixy[i][1]][sixy[i][2]] = i
        elif sixy[i][0] == -2 : #기절 산타 턴 줄이기 
            sixy[i][0] += 1
        elif sixy[i][0] == -1:
            sixy[i][0]=1
        
    #탈락하지 않은 산타에게 점수 주기
    cdie = 0
    for v in range(p): 
        if sixy[v][0] == -3:
            cdie+=1
        else:
            x= sixy[v][1]
            y= sixy[v][2]
            sr[v] +=1
    if cdie == (p):
        break

for i in range(p):
    print(sr[i], end = " ")
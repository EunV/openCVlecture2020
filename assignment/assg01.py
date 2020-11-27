#2018301044 윤웅상 01번 과제
col, row = map(int, input().split())

matrix = []
for _ in range(row):
    matrix.append(list(input()))

for r in range(row):
    for c in range(col):
        if matrix[r][c] == '*':
            print(matrix[r][c], end='', sep='')
        else:
            cnt = 0
            for y in range(r - 1, r + 2):
                if y < 0 or y >= row:
                    continue
                for x in range(c - 1, c + 2):
                    if x < 0 or x >= col:
                        continue
                    if matrix[y][x] == '*':
                        cnt += 1
            print(cnt, end='', sep='')
    print()

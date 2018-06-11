from pulp import *

numeroDeParcelas = 4
duracionCosecha = 9
D = [2, 2, 3, 2]

U = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9]]

cosecha = LpProblem('Cosecha', LpMaximize)

X = [[ pulp.LpVariable('X_%s_%s'%(i,j), lowBound=0, upBound=1, cat="Integer") for j in range(duracionCosecha)] for i in range(numeroDeParcelas)]

P = [ pulp.LpVariable('P_%s'%(i), lowBound=1, upBound=duracionCosecha, cat="Integer") for i in range(numeroDeParcelas)]

FuncionObjetivo = [(U[i][j])*(X[i][j]) for i in range(numeroDeParcelas) for j in range(duracionCosecha)]

cosecha += lpSum(FuncionObjetivo)

for i in range(numeroDeParcelas):
    cosecha += lpSum(X[i][j] for j in range(duracionCosecha)) == 1

for j in range(duracionCosecha):
    cosecha += lpSum(X[i][j] for i in range(numeroDeParcelas)) <= 1

for i in range(numeroDeParcelas):
    for j in range(duracionCosecha):
        cosecha += X[i][j]*(j + D[i] - 1) <= duracionCosecha - D[i] + 1

for i in range(numeroDeParcelas):
    for j in range(duracionCosecha - D[i] + 1):
        for fila in range(numeroDeParcelas):
            if (fila != i):
                y1 = pulp.LpVariable('Y1_%s_%s_%s'%(i,j,fila), lowBound=0, upBound=1, cat="Integer")
                y2 = pulp.LpVariable('Y2_%s_%s_%s'%(i,j,fila), lowBound=0, upBound=1, cat="Integer")
                restriccion = [X[fila][columna]*(columna + 1) for columna in range(duracionCosecha)]
                cosecha += X[i][j]*((j + 2) + D[i] - 1) <= lpSum(restriccion) + 100*(1 - y1)
                cosecha += X[i][j]*j >= lpSum(restriccion) - 100*(1 - y2)
                cosecha += y1 + y2 == 1

cosecha.solve()

print(cosecha)

for v in cosecha.variables():
    print '\t', v.name, '=', v.varValue
print '\n'

print '-------------------------\n'

for v in x.variables():
    print '\t', v.name, '=', v.varValue
print '\n'

# 
# Installation:
#   pip install numpy
#
# Start
#   https://numpy.org/doc/stable/user/quickstart.html
#
# Grundlagen
#   https://numpy.org/doc/stable/user/absolute_beginners.html
#
# Note: kommentiere die print-Anweisungen ein, 
#       die du sehen moechtest

import numpy as np

## Numpy-Arrays erstellen:
#  https://numpy.org/doc/stable/user/basics.creation.html

# Vektor mit Nulleintraegen
z1 = np.zeros(3)
print(z1)

# matrix 
z2 = np.zeros( (3,4) )
print(z2)

# ein Vektor als Liste
a = [1,2,3]
# numpy-array (automatischer Datentyp)
an = np.array(a)

print(a)
print(an)

# eine Matrix als verschachtelte Liste
b = [[1,2,3], [4,5,6], [7,8,9]]
# manuell gesetzter Datentyp
bn = np.array(b, dtype=np.float64)

# Kopie erstellen
bn_copy = np.array(bn)
# oder
bn_copy = np.copy(bn)
# oder
bn_copy = bn.copy()

#print(b)
#print(bn)

# Datentypen
#print(type(b))
#print(type(bn))
#print(bn.dtype) # datentyp der Eintraege

# Dimensionen der Matrix
#print( bn.shape )

# neues leeres Array mit der selben dimension
bnz = np.zeros( bn.shape )
#print(bnz)

# Zugriff auf ein Element bn[Zeile, Spalte]
#print( bn[1,2] )


# transponieren
bn = bn.T
#print(bn)
#print(bn.dtype)

# elementweise Multiplikation
cn = bn * bn
#print(cn)
# oder 
cn = np.multiply(bn, bn)
#print(cn)
# oder 
cn = np.multiply(bn, bn)
#print(cn)

# Matrix-Multiplikation
#dn = bn.dot(bn)
dn = bn @ bn
#print(dn)
# oder 
dn = np.dot(bn, bn)
#print(dn)
# oder 
dn = bn.dot(bn)
#print(dn)

# Matrix-Vektor Multiplikation
en = bn @ an
#print(en)
# oder 
en = bn.dot(an)
#print(en)

# Mit einer Zahl multiplizieren
#print ( bn * 3 )

# zu jeden Eintrag dieselbe Zahl addieren
#print ( bn + 3 )

# Alle Elemente aufaddieren
s = bn.sum()
#print(s)

# Maximum und Minimum
m0 = bn.min()
m1 = bn.max()
#print(m0, m1)

# Normieren
#print ( bn / bn.max() )

# Slice-Operator im Python: Schneidet eine Teilliste aus
#  List[ Begin : End : Step ]
#
#    https://www.geeksforgeeks.org/python-list-slicing/
#
#
a = [1,2,3,5,6,7]
#print( a[0:4:2] )

# Teilmatrix
#print( bn[1:,1:] )

# erste Zeile
#print( bn[0,:] )

# die ersten beiden Zeilen vertauschen
bn[[0,1], :] = bn[[1,0], :]
#print(bn)

# gesamte matrix 
#print( bn[0:3, 0:3] )

# nur gerade Spalten + Zeilen
#print( bn[0:3:2, 0:3:2] )


#!/usr/bin/python3
	
import sys

try:
	sys.argv[1]
except (IndexError, NameError):
	print ("\n!!ERROR: expected filename as an argument!!")
	filename = input("Enter name of metasprite file now: ")
else:	
	filename = sys.argv[1]
	
array = []
table = []
pallete = []
	
bg = []
meta = []

def LoadArray():
	fsrc = open(filename, 'rb')
	for i in range (0, 960):
		b = ord(fsrc.read(1))
		array.append(b)

	for i in range (960, 1024):
		b = ord(fsrc.read(1))
		pallete.append(b)
		fsrc.close

def Table2x(idx, idxSegment):
	arr = []
	arr.append(array[idxSegment])
	arr.append(array[idxSegment + 1])
	arr.append(array[idxSegment + 32])
	arr.append(array[idxSegment + 33])
	table.append(arr)

def AddPallete(idx, idxSegment):
	pal = pallete[idx]
	p = pal & 0x03
	segment = table[idxSegment]
	segment.append(p)
	table[idxSegment] = segment

	p = (pal & 0x0C) >> 2
	segment = table[idxSegment + 1]
	segment.append(p)
	table[idxSegment + 1] = segment

	if (idxSegment + 16) > 239:
		return
	p = (pal & 0x30) >> 4
	segment = table[idxSegment + 16]
	segment.append(p)
	table[idxSegment + 16] = segment

	p = (pal & 0xC0) >> 6
	segment = table[idxSegment + 17]
	segment.append(p)
	table[idxSegment + 17] = segment

def Zoom( tableSize, lineSize, func ):
	idxLine=0
	idxSegment=0
	for i in range (0, tableSize):
		if idxLine == (lineSize / 2):
			idxLine = 0
			idxSegment = idxSegment + lineSize

		func(i, idxSegment)

		idxLine = idxLine + 1
		idxSegment = idxSegment + 2

def Table2Two():

	for i in range(0, 240):
		j = 0
		while j < len(meta):
			if table[i] == meta[j]:
				bg.append(j)
				break
			j = j + 1
		if j == len(meta):
			bg.append(j)
			meta.append(table[i])

LoadArray()
Zoom(240, 32, Table2x)
Zoom(64, 16, AddPallete)
Table2Two()

fbg = open('bg.txt', 'w')
fbg.write("const unsigned char Room1[]={\n\t")
j = 0
for i in range(0, 240):
	j = j + 1
	fbg.write(str(bg[i]) + ", ")
	if j == 16:
		j = 0
		fbg.write('\n\t')
fbg.write("\r};")
fbg.close

fmeta = open('metatiles.txt', 'w')
fmeta.write("const unsigned char metatiles1[]={\n")
for i in range(0, len(meta)):
	s = ('0x{0:02x}'.format(l) for l in meta[i])
	fmeta.write(", ".join(s) + "\n")
fmeta.write("};")
fmeta.close

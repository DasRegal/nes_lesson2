#/bin/sh

name="metatiles"

CC65_HOME=../

cc65 -Oirs "$name".c --add-source
ca65 crt0.s
ca65 "$name".s -g

ld65 -C nrom_32k_vert.cfg -o "$name".nes crt0.o "$name".o nes.lib -Ln labels.txt

rm *.o

mv labels.txt ./BUILD 
mv $name.s ./BUILD 
mv $name.nes ./BUILD 

fceux BUILD/$name.nes

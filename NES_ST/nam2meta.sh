#/bin/bash

array=$($(xxd -c 1 -p < bg.nam))
table=0
bg=0
meta=0

function table2x() {
    table[$1]="0x${array[$2]}, 0x${array[$2+1]}, 0x${array[$2+32]}, 0x${array[$2+33]},"
}

function addpallete() {
    pallete="${array[$1+960]}"
    pal=$(printf "0x$pallete")
    pal_1=$(echo $((pal & 3)))
    pal=$((pal >> 2))
    pal_2=$(echo $((pal & 3)))
    pal=$((pal >> 2))
    pal_3=$(echo $((pal & 3)))
    pal=$((pal >> 2))
    pal_4=$(echo $((pal & 3)))
    table[$2]="${table[$2]} $pal_1,"
    table[$2+1]="${table[$2+1]} $pal_2,"
    table[$2+16]="${table[$2+16]} $pal_3,"
    table[$2+17]="${table[$2+17]} $pal_4,"
}

function zoom() {
    j=0
    a=0   
    for (( i=0; i<$1; i=i+1)); do
        if [[ $j == $(($2 / 2)) ]]
        then
            j=0
            let a=a+$2
        fi

        $3 $i $a

        let j=j+1
        let a=a+2
    done
}

function table2two() {
    bg[0]=0
    meta[0]="${table[0]}"
    for ((i=0;i<240;i=i+1)); do
        j=0
        while (( $j < ${#meta[*]} ))
        do
            if [[ "${table[i]}" == "${meta[j]}" ]]
            then
                bg[i]="$j"
                break
            fi
            j=$(( $j + 1))
        done
        if [[ "$j" == "${#meta[*]}" ]]; then
            bg[i]="$j"
            meta[$j]="${table[i]}"
        fi

    done
}

zoom 240 32 table2x
zoom 64 16 addpallete
table2two

j=0
var=""
echo "const unsigned char Room1[]={"
for ((i=0; i<240;i=i+1)); do
    let j=j+1
    var="$var ${bg[i]},"
    if [[ $j == 16 ]]; then
        j=0
        echo $var
        var=""
    fi
done
echo "};"

echo
echo "const unsigned char metatiles1[]={"
for ((i=0; i<${#meta[*]}; i++))
do
    echo ${meta[i]}
done
echo "};"

for ((i=0; i<240; i++))
do
    echo ${table[i]}
done


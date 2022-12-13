#/bin/bash


###################Global Variables###################
host="https://www.victim.com/FUZZ"
output_name=$(echo ffuf_$host | sed 's/https\:\/\///g' | sed 's/\/FUZZ//g' | sed 's/\./_/g' | sed 's/_$//g' | sed 's/\//_/g' | xargs)


current_folder=$(pwd)
threads=5
#if you don't use ext or filters you should modify the launch of fuff cause the behaviour will be strange.
ext=".asp,.aspx,.config,.php"
filters="-fw 6"
flag=0

####################################################
#################Global Variables###################
step=1000
start=1
finish=$(($start+$step))
last_line=$(cat directory-list-2.3-medium.txt | wc -l )
ordinary=0

####################################################



function prepare_environment(){
    if [[ -f $current_folder/directory-list-2.3-medium.txt ]] 
    then 
        echo "[*] The wordlist exists!" 
    else
        echo "[\!] The wordlist doesn't exist"
        cp /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt ./
    fi
    
    if [[ -d $current_folder/wordlists ]] 
    then 
        echo "[*] The wordlists directory exists!" 
    else
        echo "[\!] The wordlists directory doesn't exist"
        cp /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt ./
        mkdir wordlists
        split -l $step directory-list-2.3-medium.txt segment_
        mv segment_* wordlists
    fi
    



}

prepare_environment

###################################################
#Checkings


echo $$
echo "$current_folder/wordlists"
if [[ -d $current_folder/wordlists ]] 
then 
	echo "[*] The directory wordlists exists" 
else
	echo "[\!] The directory wordlists doesn't exist"
	exit 1
fi

echo "aqui..."
mkdir -p outputs
echo "alli..."

#################################################
function ctrl_c(){
  echo "[*] recopilando endpoints"
  cat $output_folder/*.json | grep -oP '"FUZZ":"(.*?)"' | sed 's/"FUZZ"://g' | tr -d '"' > $output_folder/endpoints

  echo "Saliendooooooooooooooooooooooooooooo...\n"
  exit 1
  flag=1
}

trap ctrl_c INT

######################################################

mkdir -p ffuf_logs
output_folder=$current_folder/outputs/$output_name
mkdir -p $output_folder

echo "antes del while"
while [[ $(ls wordlists | wc -l) -gt 0 ]]
do
    echo "dentro del while"
	dict=./wordlists/$(ls -l wordlists | head -2 | awk '{print $9}' | xargs)
	sufix=$(ls -l wordlists | head -2 | awk '{print $9}' | awk '{print $2}' FS="_" | xargs)
	echo "ffuf -w $(echo $dict | xargs | tr -d " ") -u $host -e $ext -o $output_folder/$output_name\_$sufix.json -of json -t $threads -c -debug-log ./ffuf_logs/log_sufix_$(echo $sufix | xargs).log $filters"
	ffuf -w $(echo $dict | xargs | tr -d " ") -u $host -e $ext -o $output_folder/$output_name\_$sufix.json -of json -t $threads -c -debug-log ./ffuf_logs/log_sufix_$(echo $sufix | xargs).log $filters
    sleep 10
	if [ $flag -eq 0 ]
    then
        rm $dict
    else
        echo "Flageando"
        exit 1
    fi
done


echo "El directorio wordlist ya no tiene fichero que leer!"
rmdir wordlists

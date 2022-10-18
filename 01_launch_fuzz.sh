if [[ -d _wordlists ]] 
then 
	echo "[*] The directory _wordlists exists" 
else
	echo "[\!] The directory _wordlists doesn't exist"
	exit(1) 
fi

mkdir outputs
###################Global Variables###################
host="https://infolog.logista.com/QvAJAXZfc/FUZZ"
output_name=$(echo ffuf_$host | tr -d "https://" | tr -d "FUZZ" | sed 's/\./_/g' | sed 's/.$//g' | xargs)


current_folder=$(pwd)
threads=3
ext=".aspx"
######################################################

mkdir -p ffuf_logs
mkdir $output_name

while [[ $(ls _wordlists | wc -l) -gt 0 ]]
do
	dict=./_wordlists/$(ls -l _wordlists | head -2 | awk '{print $9}' | xargs)
	sufix=$(ls -l _wordlists | head -2 | awk '{print $9}' | awk '{print $2}' FS="_" | xargs)
	ffuf -w $(echo $dict | xargs | tr -d " ") -u $host -e $ext -o ./ffuf_$output_name/$output_name\_$sufix.md -of md -t $threads -c -debug-log ./ffuf_logs/log_sufix_$(echo $sufix | xargs).log -or
	rm $dict
done

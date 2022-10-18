cp /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt ./
mkdir _wordlists

#################Global Variables###################
step=1000
start=1
finish=$(($start+$step))
last_line=$(cat directory-list-2.3-medium.txt | wc -l )
ordinary=0

####################################################

split -l 1000 directory-list-2.3-medium.txt segment_
mv segment_* _wordlists

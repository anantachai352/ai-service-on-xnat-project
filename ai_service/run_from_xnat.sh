#!/bin/bash -e

die() {
    echo "@" 2>&1
    exit 1
}

input="$1"
shift
project_id="$1"
shift
subject_id="$1"
shift
session_id="$1"



echo "---- echo input parameters ----"
# echo "xnat_host:" $XNAT_HOST 
# echo "xnat_user:" $XNAT_USER
# echo "xnat_pass:" $XNAT_PASS
echo "Scan file: ${input}"
echo "project_id: ${project_id}"
echo "subject_id: ${subject_id}"
echo "session_id: ${session_id}"

echo

echo "--- List ls ---"
ls ${input}
echo " ------ -------"
echo "Running Pneumonia classification"
echo "Runing script python3 main.py -i ${input} -o output/ -pro ${project_id} -subj ${subject_id} -sess ${session_id}"

mkdir output
python3 main.py -i ${input} -o output/ -pro ${project_id} -subj ${subject_id} -sess ${session_id}
echo


echo
echo "All done"
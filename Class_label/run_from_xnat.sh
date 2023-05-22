#!/bin/bash

input="$1"
shift
class="$1"
shift
output="$1"


echo "---- echo input parameters ----"
echo "Scan file: ${input}"
echo "class : ${class}"
echo "Output dir: ${output}"

echo
echo "--- List ls ---"
ls ${input}
echo " ------ -------"
echo "Running V-XNAT_Pneumonia_classification"
echo "Runing script python3 main.py -i ${input} -o ${output} -c ${class}"

python3 dicomTojpeg.py -i ${input} -o ${output} -c ${class}
echo

echo
echo "All done"
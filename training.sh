#!/bin/bash
MY_HADOOP_PYTHON="/home/sourabhbalgi/anaconda3/bin/python"  # envs/ds222_as1/
MY_HADOOP_JAR_PATH="/usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar"
MY_HADOOP_IN_DIR="/user/sourabhbalgi"
MY_HADOOP_OUT_DIR="$MY_HADOOP_IN_DIR/out_ds222_as1"

#export MY_HADOOP_PYTHON="/home/sourabhbalgi/anaconda3/bin/python"  # envs/ds222_as1/
#export MY_HADOOP_JAR_PATH="/usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar"
#export MY_HADOOP_IN_DIR="/user/sourabhbalgi"
#export MY_HADOOP_OUT_DIR="$MY_HADOOP_IN_DIR/out_ds222_as1"


#: <<'CodeBlockDisable 0'
# Create output folder to store data
echo -e "\n>>> Creating output folder out_ds222_as1 on hdfs to store output files of mapreduce. \n"
hadoop fs -mkdir $MY_HADOOP_OUT_DIR

chmod -x *.py

#hadoop fs -rm -r -f -skipTrash $MY_HADOOP_IN_DIR/*

#CodeBlockDisable 0

#: <<'CodeBlockDisable 1'
echo -e "\n>>> Starting get_classwordcount_mapred to get class word count ... \n"
hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/get_classwordcount_mapred/*
hadoop fs -rmdir $MY_HADOOP_IN_DIR/get_classwordcount_mapred

hadoop jar $MY_HADOOP_JAR_PATH \
-file "./get_classwordcount_map.py" -mapper "$MY_HADOOP_PYTHON get_classwordcount_map.py" \
-file "./get_classwordcount_red.py" -reducer "$MY_HADOOP_PYTHON get_classwordcount_red.py" \
-input "/user/ds222/assignment-1/DBPedia.full/full_train.txt" \
-output "$MY_HADOOP_IN_DIR/get_classwordcount_mapred" \
-numReduceTasks $1

echo -e "\n>>> Number of reducers used by get_classwordcount_mapred = $1. \n"

echo -e "\n>>> get_classwordcount_mapred Job completed. \n"

rm ./classwordcount.txt
echo -e "\n>>> Deleted previous file ./classwordcount.txt. \n"

# combine the output files from get_classwordcount_mapred
hadoop fs -cat $MY_HADOOP_IN_DIR/get_classwordcount_mapred/part-* > classwordcount.txt
echo -e "\n>>> Combined outputs from get_classwordcount_mapred into single file ./classwordcount.txt. \n"
hadoop fs -copyFromLocal -f ./classwordcount.txt $MY_HADOOP_OUT_DIR/
echo -e "\n>>> Copied classwordcount.txt file to hdfs output folder. \n"

#CodeBlockDisable 1

#: <<'CodeBlockDisable 2'
echo -e "\n>>> Starting get_modelparams_mapred to get model parameters ... \n"
hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/get_modelparams_mapred/*
hadoop fs -rmdir $MY_HADOOP_IN_DIR/get_modelparams_mapred

hadoop jar $MY_HADOOP_JAR_PATH \
-file "./get_modelparams_map.py" -mapper "$MY_HADOOP_PYTHON get_modelparams_map.py" \
-file "./get_modelparams_red.py" -reducer "$MY_HADOOP_PYTHON get_modelparams_red.py" \
-input "$MY_HADOOP_OUT_DIR/classwordcount.txt" \
-output "$MY_HADOOP_IN_DIR/get_modelparams_mapred" \
-numReduceTasks $1

echo -e "\n>>> Number of reducers used by get_modelparams_mapred = $1. \n"

echo -e "\n>>> get_modelparams_mapred Job completed. \n"

rm ./modelparams.txt
echo -e "\n>>> Deleted previous file ./modelparams.txt. \n"

# combine the output files from get_modelparams_mapred
hadoop fs -cat $MY_HADOOP_IN_DIR/get_modelparams_mapred/part-* > modelparams.txt
echo -e "\n>>> Combined outputs from get_modelparams_mapred into single file ./modelparams.txt. \n"
#hadoop fs -rm -skipTrash $MY_HADOOP_OUT_DIR/modelparams.txt
hadoop fs -copyFromLocal -f ./modelparams.txt $MY_HADOOP_OUT_DIR/
echo -e "\n>>> Copied modelparams.txt file to hdfs output folder. \n"

#CodeBlockDisable 2
#!/bin/bash
MY_HADOOP_PYTHON="/home/sourabhbalgi/anaconda3/bin/python"  # envs/ds222_as1/
MY_HADOOP_JAR_PATH="/usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar"
MY_HADOOP_IN_DIR="/user/sourabhbalgi"
MY_HADOOP_OUT_DIR="$MY_HADOOP_IN_DIR/out_ds222_as1"

chmod -x *.py

#: <<'CodeBlockDisable 1'
hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/$2_docwordcount_mapred/*
hadoop fs -rmdir $MY_HADOOP_IN_DIR/$2_docwordcount_mapred

hadoop jar $MY_HADOOP_JAR_PATH \
-file "./get_docwordcount_map.py" -mapper "$MY_HADOOP_PYTHON get_docwordcount_map.py" \
-file "./get_docwordcount_red.py" -reducer "$MY_HADOOP_PYTHON get_docwordcount_red.py" \
-input "/user/ds222/assignment-1/DBPedia.full/full_$2.txt" \
-output "$MY_HADOOP_IN_DIR/$2_docwordcount_mapred" \
-numReduceTasks $1

echo -e "\n>>> Number of reducers used by $2_docwordcount_mapred = $1. \n"

echo -e "\n>>> $2_docwordcount_mapred Job completed. \n"

rm ./$2_docwordcount.txt
echo -e "\n>>> Deleted previous file ./$2_docwordcount.txt. \n"

# combine the output files from $2_docwordcount_mapred
hadoop fs -cat $MY_HADOOP_IN_DIR/$2_docwordcount_mapred/part-* > $2_docwordcount.txt
echo -e "\n>>> Combined outputs from $2_docwordcount_mapred into single file ./$2_docwordcount.txt. \n"
hadoop fs -copyFromLocal -f ./$2_docwordcount.txt $MY_HADOOP_OUT_DIR/
echo -e "\n>>> Copied word count file to hdfs output folder. \n"

#CodeBlockDisable 1

: <<'CodeBlockDisable 1.5'
rm ./$2_docwordcount_modelparams.txt
echo -e "\n>>> Deleted previous file ./$2_docwordcount_modelparams.txt. \n"

hadoop fs -cat $MY_HADOOP_OUT_DIR/$2_docwordcount.txt $MY_HADOOP_OUT_DIR/modelparams.txt > $2_docwordcount_modelparams.txt
echo -e "\n>>> Combined outputs from $2_docwordcount.txt and  modelparams.txt into single file ./$2_docwordcount_modelparams.txt. \n"
hadoop fs -copyFromLocal -f ./$2_docwordcount_modelparams.txt $MY_HADOOP_OUT_DIR/
echo -e "\n>>> Copied word count file to hdfs output folder. \n"

CodeBlockDisable 1.5

#: <<'CodeBlockDisable 2''
hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/$2_postprob_mapred/*
hadoop fs -rmdir $MY_HADOOP_IN_DIR/$2_postprob_mapred

hadoop jar $MY_HADOOP_JAR_PATH \
-file "./calc_postprob_map.py" -mapper "$MY_HADOOP_PYTHON calc_postprob_map.py" \
-file "./calc_postprob_red.py" -reducer "$MY_HADOOP_PYTHON calc_postprob_red.py" \
-input "$MY_HADOOP_IN_DIR/$2_docwordcount_mapred/part-*" \
-input "$MY_HADOOP_IN_DIR/modelparams_mapred/part-*" \
-output "$MY_HADOOP_IN_DIR/$2_postprob_mapred" \
-numReduceTasks $1

echo -e "\n>>> Number of reducers used by $2_postprob_mapred = $1. \n"

echo -e "\n>>> $2_postprob_mapred Job completed. \n"

rm ./$2_postprob.txt
echo -e "\n>>> Deleted previous file ./$2_postprob.txt. \n"

# combine the output files from $2_postprob_mapred
hadoop fs -cat $MY_HADOOP_IN_DIR/$2_postprob_mapred/part-* > $2_postprob.txt
echo -e "\n>>> Combined outputs from $2_postprob_mapred into single file ./$2_postprob.txt. \n"
hadoop fs -copyFromLocal -f ./$2_postprob.txt $MY_HADOOP_OUT_DIR/
echo -e "\n>>> Copied word count file to hdfs output folder. \n"

#CodeBlockDisable 2

#: <<'CodeBlockDisable 3'
hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/$2_accuracy_mapred/*
hadoop fs -rmdir $MY_HADOOP_IN_DIR/$2_accuracy_mapred

hadoop jar $MY_HADOOP_JAR_PATH \
-file "./calc_accuracy_map.py" -mapper "$MY_HADOOP_PYTHON calc_accuracy_map.py" \
-file "./calc_accuracy_red.py" -reducer "$MY_HADOOP_PYTHON calc_accuracy_red.py" \
-input "$MY_HADOOP_OUT_DIR/$2_docwordcount_modelparams.txt" \
-output "$MY_HADOOP_IN_DIR/$2_accuracy_mapred" \
-numReduceTasks $1

echo -e "\n>>> Number of reducers used by $2_accuracy_mapred = $1. \n"

echo -e "\n>>> $2_accuracy_mapred Job completed. \n"

rm ./$2_accuracy.txt
echo -e "\n>>> Deleted previous file ./$2_accuracy.txt. \n"

# combine the output files from $2_accuracy_mapred for finding accuracy
hadoop fs -cat $MY_HADOOP_IN_DIR/$2_accuracy_mapred/part-* > $2_accuracy_predlabels.txt
echo -e "\n>>> Combined outputs from $2_accuracy_mapred into single file ./$2_accuracy_predlabels.txt. \n"
hadoop fs -copyFromLocal -f ./$2_accuracy_predlabels.txt $MY_HADOOP_OUT_DIR/
echo -e "\n>>> Copied word count file to hdfs output folder. \n"

#CodeBlockDisable 3

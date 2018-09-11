#!/bin/bash
MY_HADOOP_PYTHON="/home/sourabhbalgi/anaconda3/bin/python"  # envs/ds222_as1/
MY_HADOOP_JAR_PATH="/usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar"
MY_HADOOP_IN_DIR="/user/sourabhbalgi"
MY_HADOOP_OUT_DIR="$MY_HADOOP_IN_DIR/out_ds222_as1"

chmod +x *.py

#: <<'CodeBlockDisable1'
hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/$2_docwordcount_mapred_$1/*
hadoop fs -rmdir $MY_HADOOP_IN_DIR/$2_docwordcount_mapred_$1

hadoop jar $MY_HADOOP_JAR_PATH \
-file "./get_docwordcount_map.py" -mapper "$MY_HADOOP_PYTHON get_docwordcount_map.py" \
-file "./get_docwordcount_red.py" -reducer "$MY_HADOOP_PYTHON get_docwordcount_red.py" \
-input "/user/ds222/assignment-1/DBPedia.full/full_$2.txt" \
-output "$MY_HADOOP_IN_DIR/$2_docwordcount_mapred_$1" \
-numReduceTasks $1

echo -e "\n>>> Number of reducers used by $2_docwordcount_mapred_$1 = $1. \n"
0
echo -e "\n>>> $2_docwordcount_mapred_$1 Job completed. \n"

#CodeBlockDisable1

#: <<'CodeBlockDisable2'
hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/$2_postprob_mapred/*
hadoop fs -rmdir $MY_HADOOP_IN_DIR/$2_postprob_mapred

hadoop jar $MY_HADOOP_JAR_PATH \
-file "./calc_postprob_map.py" -mapper "$MY_HADOOP_PYTHON calc_postprob_map.py" \
-file "./calc_postprob_red.py" -reducer "$MY_HADOOP_PYTHON calc_postprob_red.py" \
-input "$MY_HADOOP_IN_DIR/$2_docwordcount_mapred_$1/part-*" \
-input "$MY_HADOOP_IN_DIR/modelparams_mapred/part-*" \
-output "$MY_HADOOP_IN_DIR/$2_postprob_mapred" \
-numReduceTasks 1

echo -e "\n>>> Number of reducers used by $2_postprob_mapred = 1. \n"

echo -e "\n>>> $2_postprob_mapred Job completed. \n"

#CodeBlockDisable2

#: <<'CodeBlockDisable3'
hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/$2_accuracy_mapred_$1/*
hadoop fs -rmdir $MY_HADOOP_IN_DIR/$2_accuracy_mapred_$1

hadoop jar $MY_HADOOP_JAR_PATH \
-file "./calc_accuracy_map_n.py" -mapper "$MY_HADOOP_PYTHON calc_accuracy_map_n.py" \
-file "./calc_accuracy_red_n.py" -reducer "$MY_HADOOP_PYTHON calc_accuracy_red_n.py" \
-input "$MY_HADOOP_IN_DIR/$2_postprob_mapred/part-*" \
-output "$MY_HADOOP_IN_DIR/$2_accuracy_mapred_$1" \
-numReduceTasks $1

echo -e "\n>>> Number of reducers used by $2_accuracy_mapred = $1. \n"

echo -e "\n>>> $2_accuracy_mapred Job completed. \n"

#CodeBlockDisable3

#: <<'CodeBlockDisable3.5'

hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/$2_accuracy_mapred/*
hadoop fs -rmdir $MY_HADOOP_IN_DIR/$2_accuracy_mapred

hadoop jar $MY_HADOOP_JAR_PATH \
-file "./calc_accuracy_map_final.py" -mapper "$MY_HADOOP_PYTHON calc_accuracy_map_final.py" \
-file "./calc_accuracy_red_final.py" -reducer "$MY_HADOOP_PYTHON calc_accuracy_red_final.py" \
-input "$MY_HADOOP_IN_DIR/$2_accuracy_mapred_$1/part-*" \
-output "$MY_HADOOP_IN_DIR/$2_accuracy_mapred" \
-numReduceTasks 1

echo -e "\n>>> Number of reducers used by $2_accuracy_mapred = 1. \n"

echo -e "\n>>> $2_accuracy_mapred Job completed. \n"


rm ./$2_accuracy_predlabels.txt
echo -e "\n>>> Deleted previous file ./$2_accuracy_predlabels.txt. \n"

# combine the output files from $2_accuracy_mapred for finding accuracy
hadoop fs -cat $MY_HADOOP_IN_DIR/$2_accuracy_mapred/part-* > $2_accuracy_predlabels.txt
echo -e "\n>>> Combined outputs from $2_accuracy_mapred into single file ./$2_accuracy_predlabels.txt. \n"
hadoop fs -copyFromLocal -f ./$2_accuracy_predlabels.txt $MY_HADOOP_OUT_DIR/
echo -e "\n>>> Copied word count file to hdfs output folder. \n"

cat ./$2_accuracy_predlabels.txt | grep '_Accuracy_'

#CodeBlockDisable3.5

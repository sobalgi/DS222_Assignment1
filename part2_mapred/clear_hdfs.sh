#!/bin/bash
MY_HADOOP_IN_DIR="/user/sourabhbalgi"
MY_HADOOP_OUT_DIR="$MY_HADOOP_IN_DIR/out_ds222_as1"

hadoop fs -ls $MY_HADOOP_IN_DIR/

hdfs dfs -rm -r "$MY_HADOOP_IN_DIR/*"
hdfs dfs -rm -r "$MY_HADOOP_IN_DIR/*"

hadoop fs -ls $MY_HADOOP_IN_DIR/

#hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/devel_calc_accuracy_mapred/*
#hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/devel_calc_postprob_mapred/*
#hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/get_docwordcount_mapred/*
#hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/get_modelparams_mapred/*
#hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/get_classwordcount_mapred/*
#hadoop fs -rm -skipTrash $MY_HADOOP_IN_DIR/out_ds222_as1/*
#
#hadoop fs -rmdir $MY_HADOOP_IN_DIR/devel_calc_accuracy_mapred/
#hadoop fs -rmdir $MY_HADOOP_IN_DIR/devel_calc_postprob_mapred/
#hadoop fs -rmdir $MY_HADOOP_IN_DIR/get_docwordcount_mapred/
#hadoop fs -rmdir $MY_HADOOP_IN_DIR/get_modelparams_mapred/
#hadoop fs -rmdir $MY_HADOOP_IN_DIR/get_classwordcount_mapred/
#hadoop fs -rmdir $MY_HADOOP_IN_DIR/out_ds222_as1/

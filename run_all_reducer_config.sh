#!/bin/bash

nohup ./training.sh 1 > word_model_001.log &  #   tail -f word_model_01.log
nohup ./training.sh 2 > word_model_002.log &  #   tail -f word_model_02.log
nohup ./training.sh 5 > word_model_005.log &  #   tail -f word_model_05.log
nohup ./training.sh 8 > word_model_008.log &  #   tail -f word_model_08.log
nohup ./training.sh 10 > word_model_010.log &  #   tail -f word_model_10.log

#copy files as backup to mirzakhani
scp -r *.* sourabh@10.192.30.14:~/prj/ds222_as1/prt2_hadoop
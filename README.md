# DS222_Assignment1
Naive Bayes classifier implementation for DBPedia dataset with 50 classes

This consists of 2 parts each included in separate folder after latest code refactoring.

1. 'part1_nb' folder has the code files and generated log files for In-Memory implementation.
the log file included train, development and test accuracies on all size of dataset( verysmall, small and full).

Also the execution times for training only, training accuracy, development accuracy and testing accuracy are logged individually for better comparisions.

To reproduce or run the In-Memory implementation, execute "./train_n_log_accuracies.sh" in terminal.



2. 'part2_mapred' folder has the codes for mapreduce implementation and appropriate logs for the number of reducers for the jobs set as 1, 2, 5, 8 and 10. The exact log files were logged from terminal using 'nohup' for correctness and automation.

To reproduce the results or evaluate the mapreduce implementation, execute the following commands.
  a. Training to get model parameters : "./training.sh numreducetask" where numreducetask is 1, 2, 5, 8 or 10.
    example : ./training.sh 10
    
  b. Testing to get predictions and accuracy : "./find_accuracy.sh numreducetask testdocument" where numreducetask is same as above and test document is (devel or test or train) for their respective accuracies.
    example : ./find_accuracy.sh 10 devel
    
    

  

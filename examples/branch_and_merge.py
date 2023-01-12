from stacklib import stack_client


# we load the stack client
stack = stack_client(key='YOUR_API_KEY')

# we connect to the coco128 dataset in YOLO format 
# (https://www.kaggle.com/ultralytics/coco128) located in the home path
stack.init(uri='coco128',  project='example_branch_and_merge')

# gets the list of datapoints
datapoints_pre_filter = stack.list_datapoints()

print(datapoints_pre_filter)

# applies a filter to get datapoints with class '1'
stack.set_filter({'1': {'class': '1'}})
datapoints_with_filter = stack.list_datapoints()
print(datapoints_with_filter)

# creates a branch of datapoints with class '1' is uri: [home]/branch_example_class_1/ 
stack.branch(uri = 'branch_example_class_1', name = 'branch with class 1', filter = {'1': {'class': '1'}})

# connects to branch
stack.init(uri='branch_example_class_1',  project='example_branch_and_merge')

datapoints_in_branch = stack.list_datapoints()
print(datapoints_in_branch)

# <----------- runs some operation on the datapoitns -----------> 

# merges the branch back to its main
stack.merge(branch = 'branch_example_class_1', main = 'coco128')
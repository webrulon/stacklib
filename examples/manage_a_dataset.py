from stacklib import stack_client

# we load the stack client
stack = stack_client(key='YOUR_API_KEY')

# we connect to the coco128 dataset in YOLO format 
# (https://www.kaggle.com/ultralytics/coco128) located in the home path
stack.init(uri='coco128',  project='example_dataset_management')

# gets the list of datapoints
datapoints = stack.list_datapoints()

print(datapoints)

# applies a filter to get datapoints with class '1'
stack.set_filter({'1': {'class': '1'}})
datapoints_with_filter = stack.list_datapoints()
print(datapoints_with_filter)

# adds a commnets to the datapoint with the filter
for datapoint in datapoints_with_filter['keys']:
    stack.comment_datapoint(datapoint, 'comment example')

# creates a slice with the contents of the filter
stack.add_slice(name = '', filter_dict = {'1': {'class': '1'}})

# resets the filter
stack.reset_filter()

# closes the session
stack.logout()
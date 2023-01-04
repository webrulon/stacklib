# Stack

### Install Stack

1. Open your favorite terminal: `Terminal`
2. Clone this repository.
3. Install stacklib: `pip install .` (ideally in a virtualenv)


### Try Stack's Python API (stack_client)

1. Import the library: ```from stacklib import stack_client```
2. Init stack in the current directory: ```stack = stack_client(key='YOUR_API_KEY')```
3. Initialize a project ```stack.init(uri='s3://mybucket/mydataset',  project='training run')```
4. Get a list of datapoints ```datapoints = stack.list_datapoints()```
5. Add comment to a datapoint ```stack.comment_datapoint(data_point_key, 'comment')```
6. Configure a training run ```stack.config = {"learning_rate": 0.001, "epochs": 100, "batch_size": 128}```
7. Log the results of a training epoch 
```stack.log({'loss': loss, 'predictions': predictions_array, 'epoch': 1})``` 
Where the predictions array is defined as: 
```predictions_array.append({'key': key, 'prediction': predictions[key], 'confidence': scores[key]})```

8. Create a branch of the dataset dataset
```stack.branch(uri = 'branch_example', name = 'branch 1', filter = [{'comment': 'comment example'}])``` 

The filter query file is an array of different dictionaries with each filter (e.g. for a computer vision dataset:[{ "class": "0" }, { "class": "1" }, { "resolution": "359x640" }, { "resolution": "333x500" }, { "tag": "comment x" }, { "box_area": [ 0, 37.15 ] }, { "date": [ "2023/1-3", "2023/1-5" ] }, { "num_classes": [ 10, 42 ] }])

9. Merge the branch to the main dataset dataset
```stack.merge(branch = 'branch_example', main = 's3://mybucket/mydataset')``` 

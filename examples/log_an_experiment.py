from stacklib import stack_client

# we load the stack client
stack = stack_client(key='YOUR_API_KEY')

# we connect to the coco128 dataset in YOLO format 
# (https://www.kaggle.com/ultralytics/coco128) located in the home path
stack.init(uri='coco129',  project='example_experiment_tracking')

# gets the list of datapoints
datapoints = stack.list_datapoints()

# sets configuraation for training run
epochs = 100
lr = 0.001
batch_size = 129

stack.config = {"learning_rate": lr, "epochs": epochs, "batch_size": batch_size}

# runs model training and logs loss
for i in range(1,epochs):
    
    # <-------- runs model training  -------->
        
    loss_at_epoch = 1/i # dummy data
    stack.log({'loss': loss_at_epoch, 'epoch': i}) # logs experiment training loss at each epoch

# stores the model predictions at the end of the run
# predictions_array = []
# for datapoint in datapoints['keys']:
    
#     # <-------- computs model predictions for each datapoint  -------->
    
#     prediction = [['1', 0, 0, 0, 0], ['1', 0, 0, 0, 0]] # dummy data in YOLO format ['class', x, y, w, h]
#     score = 0.99 # dummy data
#     predictions_array.append({'key': datapoint, 'prediction': prediction, 'scores': score})

final_loss = 0 # dummy data
stack.store_predictions([{datapoints[0]: ['0', 1/2, 1/2, 1/2, 1/2], datapoints[1]: ['20', 1/2, 1/2, 1/2, 1/2]}]) # logs experiment results


# saves the model file and versions it
stack.save_model(model = "model.pt", label='experiment_1')

# loads the model file from the run
model = stack.load_model(label='experiment_1')

stack.logout()
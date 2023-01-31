import requests
import math
import random

class stack_client():
    def __init__(self, key=''):
        super().__init__()
        self.status = None
        self.address = 'http://localhost:8000/'

        self.project = None
        self.uri = None

        self.config = {}

    def init(self, uri, project):
        self.uri = uri
        self.project = project
        response = requests.get(self.address+ "init_experiment", json={'uri': uri, 'project': project})
        return response.json()
    
    def log(self, data):
        response = requests.post(self.address+'add_log', json={'log': data, 'config': self.config, 'project': self.project, 'uri': self.uri})
        return response.json()

    def store_predictions(self, data):
        response = requests.post(self.address+'add_predictions', json={'prediction': data, 'config': self.config, 'project': self.project, 'uri': self.uri})
        return response.json()

    def list_datapoints(self, n_start = -1, n_end=-1):
        if n_start == -1 and n_end == -1:
            len = requests.get(self.address+'current?page=0&max_pp=1')
            response = requests.get(self.address+"current?page=0&max_pp="+str(len.json()['len']))
            return response.json()
        else:
            res = requests.get(self.address+'current?page=0&max_pp=1')
            len = dict(res.json())['len']
            datapoints = {'keys': [], 'lm': []}
            
            if n_start == -1 or n_start == 0:
                iters = 1
                start = 0
                n_start = n_end
            else:
                iters = math.floor(n_end/n_start)
                start = 0
                if n_end == -1:
                    iters = math.floor(len/n_start)

            if iters > 1:
                for k in range(start, iters):
                    response = requests.get(self.address+"current?page="+k+"&max_pp="+n_start)
                    response = dict(response.json())
                    datapoints['keys'].extend(response['keys'])
                    datapoints['lm'].extend(response['lm'])                
                response = requests.get(self.address+"current?page="+iters+"&max_pp="+n_start)
                response = dict(response.json())
                datapoints['keys'].extend(response['keys'][:n_end%n_start])
                datapoints['lm'].extend(response['lm'][:n_end%n_start])
            else:
                response = requests.get(self.address+"current?page="+0+"&max_pp="+n_start)
                response = dict(response.json())
                datapoints['keys'].extend(response['keys'][:n_end%n_start])
                datapoints['lm'].extend(response['lm'][:n_end%n_start])

            return datapoints
    
    def load_dataset(self, version=None, slice=None, branch=None, n_start = -1, n_end=-1):
        datapoints = self.list_datapoints(n_start=n_start, n_end=n_end)
        dataset = []
        # for key in datapoints['keys']:
        #     res = requests.get(self.address+f"get_datapoint?{key}")
        #     dataset.append(res.json)
        return dataset

    def list_models(self):
        response = requests.get(self.address+"get_models")
        return dict(response.json())
    
    def add_file(self, filename):
        file = {'file': open(filename ,'rb')}
        url = self.address+'add_multifiles'

        response = requests.post(url=url, files=file)
        return dict(response.json())['success']

    def save_model(self, model, label):
        data = {'data': '{"label": "'+label+'"}'}
        file = {'file': open(model ,'rb')}
        url = self.address+'add_model'

        response = requests.post(url=url, data=data, files=file)
        return dict(response.json())['success']

    def load_model(self, label):
        response = requests.get(self.address+'get_model', json={'project': self.project, 'label': label})
        return response.content

    def comment_datapoint(self, key, comment):
        response = requests.get(self.address+"add_tag?file="+key+'&tag='+comment)
        return dict(response.json())['success']

    def add_datapoint(self, key):
        response = requests.get(self.address+"add_datapoint?key="+key)
        return dict(response.json())['success']

    def get_labels(self, key):
        response = requests.get(self.address+"get_labels?key="+key)
        return dict(response.json())

    def set_labels(self, key, label):
        data = {'keyId': key, 'Label': label}
        response = requests.get(self.address+"set_labels",json=data)
        return dict(response.json())
    
    def uncomment_datapoint(self, key):
        response = requests.get(self.address+"remove_all_tags?file="+key)
        return dict(response.json())['success']

    def set_filter(self, filter_dict):
        response = requests.get(url=self.address+"set_filter", data=filter_dict)
        return dict(response.json())['success']

    def reset_filter(self):
        response = requests.get(url=self.address+"reset_filters")
        return dict(response.json())['success']

    def add_slice(self, name, filter_dict = None):
        if filter_dict:
            _ = requests.get(url=self.address+"set_filter", data=filter_dict)
        response = requests.get(url=self.address+"add_slice?slice_name="+name)
        if filter_dict:
            _ = requests.get(url=self.address+"reset_filters")
        return dict(response.json())['success']

    def branch(self, uri, title = None, type='copy', filter = None):
        if title == None:
            title = uri

        if filter:
            _ = requests.get(url=self.address+"set_filter", data=filter)
        data = {'branch_name': uri, 'branch_title': title, 'branch_type': type}
        response = requests.get(url=self.address+"set_branch",data=data)
        if filter:
            _ = requests.get(url=self.address+"reset_filters")
        return dict(response.json())['success']

    def merge(self, branch = None, main = None):
        if branch:
            if main:
                data = {'child': branch, 'parent': main}
                response = requests.get(url=self.address+"merge",data=data)        
                return dict(response.json())['success']
            else:
                response = requests.get(url=self.address+"merge_child_to_master?uri="+branch)        
                return dict(response.json())['success']
        else:
            response = requests.get(url=self.address+"merge_current_to_master")
            return dict(response.json())['success']

    def logout(self):
        response = requests.get(self.address+"logout_experiment")
        return dict(response.json())['success']


if __name__ == '__main__':
    stack = stack_client(key='YOUR_API_KEY')

    # we connect to the coco128 dataset in YOLO format 
    # (https://www.kaggle.com/ultralytics/coco128) located in the home path
    stack.init(uri='mini_squad',  project='Davinci3 finetune')

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
        loss_at_epoch = 1/i + random.random()/4 # dummy data
        stack.log({'loss': loss_at_epoch, 'epoch': i}) # logs experiment training loss at each epoch

        # stores the model predictions at the end of the run
        # predictions_array = []
        # for datapoint in datapoints['keys']:
            
        #     # <-------- computs model predictions for each datapoint  -------->
            
        #     prediction = [['1', 0, 0, 0, 0], ['1', 0, 0, 0, 0]] # dummy data in YOLO format ['class', x, y, w, h]
        #     score = 0.99 # dummy data
    #     predictions_array.append({'key': datapoint, 'prediction': prediction, 'scores': score})
    pred = {}
    for i in range(10):
        pred[datapoints['keys'][i]] = [['0', 1/2, 1/2, 1/2, 1/2]]
    stack.store_predictions([pred]) # logs experiment results


    # saves the model file and versions it
    stack.save_model(model = "model.pt.txt", label='experiment_1')

    # loads the model file from the run
    model = stack.load_model(label='experiment_1')

    stack.logout()
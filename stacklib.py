import requests
import math

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

    def branch(self, uri, title = None, type='copy', filter_dict = None):
        if title == None:
            title = uri

        if filter_dict:
            _ = requests.get(url=self.address+"set_filter", data=filter_dict)
        data = {'branch_name': uri, 'branch_title': title, 'branch_type': type}
        response = requests.get(url=self.address+"set_branch",data=data)
        if filter_dict:
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

    stack = stack_client(key='NA')
    stack.init(uri='s3://mydatasets/coco129',  project='training run')

    dset = stack.load_dataset(version='-1',slice=None,branch=None)

    datapoints = stack.list_datapoints()
    stack.config = {"learning_rate": 0.001, "epochs": 100, "batch_size": 128}
    
    for i in range(1,100):
        # Runs model training
        dp_predictions = []
        for key in datapoints['keys']:
            dp_predictions.append({'key': key, 'prediction': predictions[key], 'scores': scores[key]})
        stack.log({'loss': 1/i, 'prediction': dp_predictions, 'epoch': i})
    
    stack.save_model(model = "model.pt", label='v1')
    model = stack.load_model(label='v1')

    stack.logout()
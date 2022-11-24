import requests
import math

class stack_client():
    def __init__(self, key='') -> None:
        super().__init__()
        self.status = None
        self.address = 'localhost:8000/'

        self.project = None
        self.uri = None
        
        self.config = {}

    def init(self, uri, project):
        self.uri = uri
        self.project = project
        response = requests.get(self.address+f'init_experiment', json={'uri': uri, 'project': project})
        return response.json['success']
    
    def log(self, data):
        response = requests.post(self.address+'add_log', json={'log': data, 'config': self.config, 'project': self.project, 'uri': self.uri})
        return response.json['success']

    def list_datapoints(self, n_start = -1, n_end=-1):
        if n_start == -1 and n_end == -1:
            len = requests.get(self.address+f'current?page=0&max_pp=1')
            response = requests.get(self.address+f"current?page=0&max_pp={len.json['len']}")
            return response.json
        else:
            res = requests.get(self.address+f'current?page=0&max_pp=1')
            len = res.json['len']
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
                    response = requests.get(self.address+f"current?page={k}&max_pp={n_start}")
                    datapoints['keys'].extend(response['keys'])
                    datapoints['lm'].extend(response['lm'])

                
                response = requests.get(self.address+f"current?page={iters}&max_pp={n_start}")
                datapoints['keys'].extend(response['keys'][:n_end%n_start])
                datapoints['lm'].extend(response['lm'][:n_end%n_start])
            else:
                response = requests.get(self.address+f"current?page={0}&max_pp={n_start}")
                datapoints['keys'].extend(response['keys'][:n_end%n_start])
                datapoints['lm'].extend(response['lm'][:n_end%n_start])

            return datapoints
    
    def load_dataset(self, n_start = -1, n_end=-1):
        datapoints = self.list_datapoints(n_start=n_start, n_end=n_end)
        dataset = []
        for key in datapoints['keys']:
            res = requests.get(self.address+f"get_datapoint?{key}")
            dataset.append(res.json)
        return dataset

    def list_models(self):
        response = requests.get(self.address+f"get_models")
        return response.json
    
    def save_model(self, model, label):
        response = requests.post(self.address+'add_model', files={'file': model}, json={'project': self.project, 'label': label})
        return response.json['success']

    def load_model(self, label):
        response = requests.post(self.address+'get_model', json={'project': self.project, 'label': label})
        return response.file

    def tag_datapoint(self, key, tag):
        response = requests.post(self.address+f'add_tag?tag={tag}&file={key}')
        return response.json['succes']

if __name__ == '__main__':
    client = stack_client(key='')
    client.init(uri='coco129', project='test1')

    dp = client.list_datapoints()
    dset = client.load_dataset()

    models = client.list_models()
    
    f = open("model.pt", "w")
    f.write("this is the model")
    f.close()
    model = open("model.pt", "rb")
    
    client.save_model(model = model, label='model1')
    model = client.load_model(label='model1')


    client.tag_datapoint(dp['keys'][0], 'tag addded programatically')
    
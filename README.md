# eos_cloud

1. box to point
2. point to Imglable box
3. mannual adjust
4. xml to csv

## Model Serving

### Build Container

gcloud compute instances create $VM_NAME --machine-type n1-standard-4 --image=coreos-stable-2247-5-0-v20191016 --image-project=coreos-cloud

gcloud compute scp --compress --recurse model_container/ $VM_NAME:~/

gcloud compute ssh $VM_NAME

(IN VM)

https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

export PATH="$HOME/miniconda3/bin:$PATH"
source $HOME/miniconda3/bin/activate

docker pull tensorflow/serving

docker run -d --name serving_base tensorflow/serving 

export MODEL_NAME=eos
export MODEL_P=eos

(MODEL_P is the path of dir which is a model's version dir's parent dir, and **saved_model.pb is in the version dir**. In other words, it looks like MODEL_P/123456/saved_model.pb)

docker cp $MODEL_P serving_base:/models/$MODEL_NAME

docker commit --change "ENV MODEL_NAME $MODEL_NAME" serving_base $MODEL_NAME

docker kill serving_base
docker rm serving_base

export PORT=8501

docker run -p $PORT:$PORT -t $MODEL_NAME &

(USEDUL CML: 
docker ps
docker stop (docker ps -aq)
for n in $(find DIR -type f [-not] -name "*jpg")); do python XX.py $n > $(basename ${n%.\*}); done

(TEST model status)

curl -XGET 'localhost:$PORT/v1/models/$MODEL_NAME/{versions/$VERSION}'

curl -XGET 'localhost:$PORT/v1/models/$MODEL_NAME/{versions/$VERSION}/metadata'

### Use VM to Demo

### OR Use App Engine to Demo

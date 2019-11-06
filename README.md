
#  Detect Eosinophils on GCP
  
This article is an end-to-end demonstration of how to create and deploy a computer vision model on Google Cloud.

Demo [**HERE**](https://eosnext-o5jdmxcucq-uc.a.run.app).

Test Slides are provided on Google Drive, click [**HERE**](https://drive.google.com/file/d/13lXgS3ZmFv3YtQhQAzb5Iw8Mf2DOkmI5/view).

In this process, I will reuse the data form one of my previous projects. I will process the data to match the request format of Google Cloud's AutoML Vision, first. Then, I will leverage the AutoML Vision to train an "object detection" model on these precessed data. Next, I will deploy the model on Google Cloud's Kubernetes Engine (GKE). Finally, I will use Cloud Run to implement a stateless website to show how the model work.
  
Now, please let me guide you to walk through the journey.
The story has five parts. They are :
  
1. The way I used to play
  
2. Start again
  
3. Magic -- AutoML Vision
  
4. Lift and serve the model
  
5. Create a stateless Web-APP
  
6. Deploy in one way or another way
  
##  The way I used to play
  
It's a long hot summer night. I was sitting in front of my desktop, trying to adjust the parameter of my *little* watershed algorithm so that it can nicely separate the background and my interest of regions -- [Eosinophils](https://en.wikipedia.org/wiki/Eosinophil).
  
This project was set up by Data and Computer Science department, Sun Yat-sen University, and Sun Yat-sen memorial hospital. It aims to build a framework that could be used to train a model to "learn" any types of cells they want to detect. And the first type they chose is the Eosinophils, which is vital in clinical testing and somewhat easy to be recognized.
  
Two other medical students and I were invited to try the water. The model was supposed to be used in personal computers, especially laptops. We started with three labeled slides. On each of the slides, there are about 100 - 200 Eosinophils. The figure below is an example.
  
![Our starting point](https://drive.google.com/uc?id=1J51vxy0B5uJzOhMlsfiWlqQyG0ykbsJB  "Our starting point")
  
I had read some articles about object detection. I tried to use [Google's object detection API](https://github.com/tensorflow/models/tree/master/research/object_detection) in Tensorflow to train a model, which is based on faster-RCNN architecture. It failed, of course, simply because the number of images is too small. Also, I realized the model of faster-RCNN that is one hundred more MB, which is quite large, and it is not possible to run on ordinary laptops fast. Luckily, Kaggel has hosted [a competition](https://www.kaggle.com/c/data-science-bowl-2018) about cell detections at that moment. From that competition, I met a model architecture, [U-net](https://en.wikipedia.org/wiki/U-Net). Many teams in that competition successfully used this architecture. Moreover, it's fast, relatively small, and powerful, which fitted our users' needs. Still, three slides were not enough.
  
So the first thing was to get enough data. We decided to train a CNN model, which is easy to be created, to help us label slides. First, we used watershed and other algorithms to segment cell-like "tiles" from the slides. Then, we used these small images to train a classification CNN model. The model worked well. And we used it to classify the cell-like objects segmented by a watershed algorithm on unlabeled slides. It's an indirect way to label slides. After that, we just corrected the wrong label, and we could get labeled slides super quickly because the CNN model has labeled many cells. The result like the below. The boxed are the labels made by the model, and we used green points to "correct" its labels.
  
![We corrected CNN's mistakes](https://drive.google.com/uc?id=188V0uw_eD-3sx6Y603XivMUstowt6w9b  "We corrected CNN's mistakes")
  
After we had 40 to 50 slides, we began to use U-net as the architecture for our next model. However, U-net can only generate a possibility hot-map and needs hot-maps to train. Remember what the users asked is the count of cells, not a possibility hot map. So the U-net model cannot work alone, and we had to design a pipeline to have other components complementing the U-net model. 
For training, first, we cropped each large slide into small images. Then, we used watershed algorithms to "transform" our previous label as "masks" so that U-net can be trained. When it comes to prediction, we cropped the slide for prediction into small images first; next, we used U-net to generate masks; then, masks were combined into a large mask to match the original slide. Finally, we use watershed and other algorithms to detect the region of cells. Because after U-net's processing, the masks will show the interest of regions as white and the background as black. It's easy for the watershed to separate the cells from this pure background. The final result and its mask are shown below. Then, we had done it!

![Mask and its final result](https://drive.google.com/uc?id=1mFYZz77HTRM0LGBbKYvzPms9HwSTUbux)

For more details, look at in [here](https://github.com/Moo-YewTsing/EOS-Detection)
  
##  Start again
  
I have to admit it's a complicated process. And the tuning process for the watershed algorithm was an unpredictable and trial-and-error experiment, or say torture. Due to the different sizes and overlapping ways of cells, it's hard to adjust the parameters to fit all situations manually. Also, because the watershed algorithm has the final say, the ceiling of the model's performance is restricted by this old-fashion algorithm. As a result, even though the U-net works well, the overall precision is 0.81, and the recall is just 0.72.
  
From Coursera, I knew the [AutoML Vision of Google Cloud](https://cloud.google.com/vision/automl/docs/) is impressive. So I decided to have a try. The data to train an object detection, it needs, are images and label boxes' coordinates. However, what I have are slides with points and boxes. I tried to use the watershed algorithm again to "transform" these labels to coordinates. The result was terrible, which has a lot of repeating coordinates. It's not a problem to prepare data for the U-net model, because the data it feeds on are masks, which will not be influenced by repeating. However, for this end-to-end prediction model, it will directly learn from the bad data. As a result, it will learn the repeating labels are different and cause serious over-counting.
  
I found the size of the cells is similar. Also, the loss function of the AutoML Vision model is based on [mAP](https://medium.com/@jonathan_hui/map-mean-average-precision-for-object-detection-45c121a31173). It means the location and coverage of the label box don't need to be exactly accurate. So, I began to re-label all the labeled slides, whether they are labeled by yellow points or black boxes, by green points. Then, I calculated a box with each point as the middle, and with a randomly normal distributed change in line length. I saved these box label data into XML files so that I can use [LabelImg](https://github.com/tzutalin/labelImg) to check and make a manual adjustment. Always "junk in junk out", and data quality must be checked. Finally, I convert these XML files into CSV files and change the line absolute length (pixel) into relative length, as required by AutoML Vision.
  
![Prepare Data](https://drive.google.com/uc?id=16ZjI1seLklatJOIB_89k4YmqBwtJm76Y  "Prepare Data")
  
##  Magic -- AutoML Vision
  
The architecture of the vision models is in secret. Still, from the model's respond payload, I saw the AutoML Vision would resize the images into 512 \* 512 pixels. Also, as a rule of thumb, to get a smaller model, every input instance should be smaller. So I divided each 1920 \* 1440 slides into four 960 \* 720 images and changed their labels value correspondingly.
  
Locally, I randomly separate the whole data into the training dataset and the testing dataset. Then, the training dataset and its label CSV were uploaded to Cloud Storage. I measured the different performances between Cloud Served Model (the big one) and Edge Model (the small one) in varying settings. Cloud Served Model cannot be extracted from the Cloud, so I cannot adjust the threshold nor move the model to other places. The comparison is as below.
  
![Mobile Low Latency](https://drive.google.com/uc?id=1F_OrHVkjsiUZCWFEYMLqvbPg2-_y3aox  "Mobile Low Latency")
  
![Mobile High Accuracy](https://drive.google.com/uc?id=1llyAvG0mg7rt8EAMsIV57r2BSa5XlZMr  "Mobile High Accuracy")
  
![Cloud High Accuracy](https://drive.google.com/uc?id=1qYJAqL2JRKax7lZZWBiHKbdm4FbUx3x7  "Cloud High Accuracy")
  
The edge model in the "Mobile High Accuracy" type performs well and can be used in other places. It's an excellent option to leverage the expertise of Google AI. So, I extracted it out and prepared to deploy it.
  
##  Lift and serve the model
  
Here come at least three solutions.
  
First, simply click the "Deploy Model", and GCP will handle all the process and network tuning related to deployment. It's auto-scale up as well. However, one downside is that it'll *help* to filter the result, and then, only the outcome with possibilities larger than 0.5 will be sent back from the server. Also, the price is $0.0791 per node per hour, which is higher than the following options.
  
Second, you can deploy the model by yourself, and using docker to make the model service containerized is the option. It's super fast to write a Dockerfile based on [TensorFlow Serving](https://github.com/tensorflow/serving) and use [Google Build](https://cloud.google.com/cloud-build/) to wrap the model into a container and deploy it to the places you want. For example, you can choose [Kubernetes](https://cloud.google.com/kubernetes-engine/), "a managed, production-ready environment for deploying containerized applications". A "cluster" with only one small machine type is enough for this model, which has 0.5 CPUs and 1.7GB RAM, costing only $0.0257 per hour.
  
Last, to achieve maximum DIY, you can choose to use a VM and do what you want. But, in this case, you have to set the networking forwarding rules, safety rules, etc..
  
Here I chose the second solution and used the power of Kubernetes. I changed part of the Dockerfile of TensorFlow Serving to make the REST port follow the container's environment variables. Then, I used Cloud Build to create a container image based on the Dockerfile. Cloud Build automatically submitted the image to the Container Registry, "a single place to manage Docker images", which is on the Cloud Storage, so that the other service can use this image immediately.
  
After creating a cluster as the description above, I deployed the container to the cluster using Kubernetes. On the cluster, Kubernetes create two pods for running model and one pod as load balancer and exporting REST API. Then, this microserver for Eosinophils detection was deployed and can be used anywhere.
  
##  Create a stateless Web-APP
  
To show the performance of this model, I made a Web-APP adapting form one Github [repository](https://github.com/lucleray/object-detection/). Next.js build it. I'm not a Web-APP developer, so this app is almost just a copy-paste-change product. Under the hood, it reads the local image, converts it into Base64 string in JSON, and calls the REST API of the model served by Kubernetes. Also, because this Web-APP can be containerized, I can use Kubernetes as well. Here, for the propose of saving money, I use [Cloud Run](https://cloud.google.com/run/), "a managed to compute platform that automatically scales your stateless containers."
  
It sounds like Kubernetes. Yes, it's abstracting Kubernetes, and all you need to do is to provide a container. I think my model can be served in this way, as well. Since Cloud Run will bill you by request, it can idle on the Cloud and cost 0. Yet, the Kubernetes is charged on the running hour of the clusters, so it's like a flat price. If you want to listen to the call 24 hours a day, you have to pay 24 hours, no matter how many requests your server handles. For a project aiming to show a prototype can work, i.e., only 1 or 2 requests exist, Cloud Run will be much cheaper, maybe stay at the free tier.
  
Again, demo [**HERE**](https://eosnext-o5jdmxcucq-uc.a.run.app). Test Slides are provided on Google Drive, click [**HERE**](https://drive.google.com/file/d/13lXgS3ZmFv3YtQhQAzb5Iw8Mf2DOkmI5/view).
  
![How it looks](https://drive.google.com/uc?id=10xartG0QqZbcOyToH3MojrLuka6bga-V  "How it looks")
  
Want to have a look at the Github repository of this Web-APP? [**Here**](https://github.com/Moo-YewTsing/eos-next-web) you go!
  
##  Delopy in one way or another way
  
Here is the whole architecture.
  
![Architecture](https://drive.google.com/uc?id=1gCOgbKT6Kt14wwxo-vQx91KcQmyvx_Aw  "Architecture")
  
You can notice that between the Web-APP and the model server is a layer called "[Cloud Functions](https://cloud.google.com/functions/)". It's "a serverless compute platform that makes it easy to run and scale your code in the cloud". I used it to hide my model server API and as an interface for future additions.
  
And because every part is a microserver, you can change one server or add more servers without influencing the other parts. For example, if I want to add authentication, I can use Cloud Functions to add a layer between the Web-APP and the Cloud Functions or add some code in the Cloud Functions. Meanwhile, use another container as a database to provide authentication information. And then it's done.

Wander what the advantage of this "microserver" architecture is? Have a look at one [**Presentation**](https://www.youtube.com/watch?v=IblDMVwSSk4&list=PL5eBvoNpSYNuLeXA6empS77NarQXkumLi&index=63&t=6s) from *Google Cloud Next 2019*. Here are two take-home captures from it.

Thanks!
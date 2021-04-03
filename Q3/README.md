- Install minikube, kubeadm, kubectl using apt command
- Start minikube
 `minikube start`
- Clone the repo from https://github.com/dmontag23/qa-streaming-pipeline-challenge
- Install kompose - https://github.com/kubernetes/kompose/blob/master/docs/installation.md#github-release
- Build the images for frontend and backend using command from Dockerfile in the respective folders 
```
docker build -t sairaghav/qa-challenge-frontend .
docker build -t sairaghav/qa-challenge-backend .
```

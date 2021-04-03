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
- Push the images to docker hub as a public repository
```
docker push sairaghav/qa-challenge-frontend
docker push sairaghav/qa-challenge-backend
```
- Use `kompose convert` command from the folder where docker-compose.yml file is located to create the deployment and service configuration files
- Modify the spec.container.build parameter to spec.container.image parameter with the images pushed in the previous step for both frontend and api

*frontend-deployment.yaml*
```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    io.kompose.service: frontend
  name: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      io.kompose.service: frontend
  template:
    metadata:
      labels:
        io.kompose.service: frontend
    spec:
      containers:
        - image: sairaghav/qa-challenge-frontend
          name: frontend
          ports:
            - containerPort: 3000
      restartPolicy: Always
status: {}
```

*api-deployment.yaml*
```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    io.kompose.service: api
  name: api
spec:
  replicas: 1
  selector:
    matchLabels:
      io.kompose.service: api
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        io.kompose.service: api
    spec:
      containers:
        - image: sairaghav/qa-challenge-backend
          name: api
          ports:
            - containerPort: 5000
          resources: {}
          volumeMounts:
            - mountPath: /web
              name: api-claim0
      restartPolicy: Always
      volumes:
        - name: api-claim0
          persistentVolumeClaim:
            claimName: api-claim0
status: {}
```
- The value of replicas and the template can be adjusted as required.

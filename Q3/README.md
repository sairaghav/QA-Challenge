# Getting Started
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

# Configuring deployment and services
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
```
- The value of replicas and the template can be adjusted as required.

- Configure the services for frontend and the api as follows:
*frontend-service.yaml*
```
apiVersion: v1
kind: Service
metadata:
  labels:
    io.kompose.service: frontend
  name: frontend
spec:
  type: NodePort
  ports:
    - name: frontend
      port: 3000
      targetPort: 3000
  selector:
    io.kompose.service: frontend
```
*api-service.yaml*
```
apiVersion: v1
kind: Service
metadata:
  labels:
    io.kompose.service: api
  name: api
spec:
  type: NodePort
  ports:
    - name: http
      port: 5000
      targetPort: 5000
  selector:
    io.kompose.service: api
```

- The `type` is configured as `NodePort` to allow access for debugging. In case, this is to be exposed to the internet, configure `type` as `LoadBalancer`
- `nodePort` can optionally be specified explicitly to allow access to that specific port.
- Deploy the cluster using command: `kubectl apply -f api-claim0-persistentvolumeclaim.yaml,api-deployment.yaml,api-service.yaml,frontend-deployment.yaml,frontend-service.yaml`

# Verifying configuration
- Status of deployment
![image](https://user-images.githubusercontent.com/4383992/113478603-1f82de00-948a-11eb-8e58-f1a4238f0d37.png)

- Service Information

![image](https://user-images.githubusercontent.com/4383992/113478684-a33cca80-948a-11eb-8969-d1de271edf26.png)


- Verifying access

**Frontend**

![image](https://user-images.githubusercontent.com/4383992/113478806-7dfc8c00-948b-11eb-9275-e7f775ec6625.png)

**API**

![image](https://user-images.githubusercontent.com/4383992/113478797-6c1ae900-948b-11eb-8c6f-34bbc8bec3e1.png)

# Configure access with URL
- Enable ingress add-on from minikube with command: `minikube addons enable ingress`
- Configure `ingress.yaml` to define host `streaming.quickalgorithm.com` and paths for access api and the frontend
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: streaming.quickalgorithm.com
      http:
        paths:
          - pathType: Prefix
            path: /api
            backend:
              service:
                name: api
                port:
                  number: 5000

          - pathType: Prefix
            path: /
            backend:
              service:
                name: frontend
                port:
                  number: 3000
```
- This will load the frontend when calling `streaming.quickalgorithm.com` and to the api when calling `streaming.quickalgorithm.com/api`
- Apply the ingress rules with command `kubectl apply -f ingress.yaml`
- Configure `/etc/hosts` file to resolve to NodeIP when `streaming.quickalgorithm.com` is queried. Ideally, this is configured in Route53 or Google Domain when using cloud providers.
![image](https://user-images.githubusercontent.com/4383992/113479089-2fe88800-948d-11eb-8a13-e49a8adf901d.png)


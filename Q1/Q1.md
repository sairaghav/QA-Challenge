1. Login to the server using the SSH key 
```
chmod 400 my-key-pair.pem 
ssh -i my-key-pair.pem <user>@remote-server-ip
```

2. Install docker and docker-compose binaries
```
apt-get install docker.io
apt-get install docker-compose #Installing docker-compose first also installs docker.io as it is a dependency
```

3. Add current user to docker group to ensure access to docker without sudo
```
sudo groupadd docker
sudo usermod -aG docker $USER
```

**Assumptions**
- User has sudo privilege to add group and modify user permission

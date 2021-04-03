- Start docker service using the command:
`
sudo systemctl start docker
`

- Check for memory allocated to docker service with the command:
`
ps aux | {head -1; grep docker}
`
```
RSS -> Gives the current memory used by the process
VSZ -> Gives the total memory allocated to the process
```
- The resources allocated to the process can also be monitored using `top` command by providing the process id collected from `ps aux` result:
`
top -x <pid>
`

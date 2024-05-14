# <p align="center">My little ansible</p>
  
MyLittleAnsible is a Python command-line program designed to configure remote hosts using Infrastructure as Code (IaC) principles. It allows you to automate system configuration tasks on remote hosts, leveraging a declarative approach to infrastructure setup. In this exemple i's for two Virtual machines.


### Execution of Todos

MyLittleAnsible executes tasks defined in a YAML file (todos.yml). Tasks include managing packages, copying files, templating configurations, and administering systemd services.

### SSH Authentication

MyLittleAnsible supports three methods of SSH authentication:

- Default SSH configuration
- Username/password authentication
- Private key authentication

### Inventory Management

Define the hosts to configure in an inventory file (inventory.yml). Each host includes SSH connection details such as address and port.

### Execution Modules

- `copy`: Copy files or directories to remote hosts.
- `template`: Render Jinja2 templates on remote hosts.
- `service`: Manage systemd services on remote hosts.
- `sysctl`: Modify kernel parameters on remote hosts.
- `apt`: Manage APT packages on remote hosts.
- `command`: Execute arbitrary shell commands on remote hosts.


### Screen
![Cover](https://github.com/Haroun-Azoulay/python_MyLittleAnsible/blob/main/img/ansible.png)
        
## 🛠️ Tech Stack
- [Python](https://www.python.org/)

## 🧐 Features         
- [Paramiko](https://www.paramiko.org/)
- [Click](https://click.palletsprojects.com/en/8.1.x/)
- [Jinja](https://jinja.palletsprojects.com/en/3.0.x/)
    
 
## 🛠️ Install Dependencies    

### Docker image building

```bash
docker build -t my_image:tag .
```
### Docker run

```
docker run --network host -ti ansible  my_image:tag
```

## ❤️ Support  
A simple star to this project repo is enough to keep me motivated on this project for days. If you find your self very much excited with this project let me know with a tweet.

## 🙇 Author
#### Haroun Azoulay
- Github: [@Haroun-Azoulay](https://github.com/Haroun-Azoulay)

# Ansible Cheatsheet for MLOps/DevOps Engineers

## Installation & Setup

### Install Ansible
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ansible -y

# RHEL/CentOS
sudo yum install ansible -y

# macOS
brew install ansible

# Using pip
pip install ansible

# Using pipx (recommended)
pipx install ansible

# Verify installation
ansible --version
```

### Initial Configuration
```bash
# Create Ansible configuration file
mkdir -p ~/.ansible
cat > ~/.ansible/ansible.cfg << 'EOF'
[defaults]
inventory = ~/ansible/inventory
host_key_checking = False
retry_files_enabled = False
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 3600
interpreter_python = auto_silent

[privilege_escalation]
become = True
become_method = sudo
become_user = root
become_ask_pass = False
EOF

# Create inventory directory
mkdir -p ~/ansible/{inventory,playbooks,roles}
```

---

## Inventory Management

### Basic Inventory (INI Format)
```ini
# inventory/hosts.ini
[mlops_servers]
ml-train-01 ansible_host=192.168.1.10
ml-train-02 ansible_host=192.168.1.11

[api_servers]
ml-api-01 ansible_host=192.168.1.20
ml-api-02 ansible_host=192.168.1.21

[monitoring]
prometheus ansible_host=192.168.1.30
grafana ansible_host=192.168.1.31

[mlops:children]
mlops_servers
api_servers
monitoring

[mlops:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_rsa
python_version=3.11
```

### Inventory (YAML Format)
```yaml
# inventory/hosts.yml
all:
  children:
    mlops_servers:
      hosts:
        ml-train-01:
          ansible_host: 192.168.1.10
        ml-train-02:
          ansible_host: 192.168.1.11
      vars:
        gpu_enabled: true
        cuda_version: "11.8"
    
    api_servers:
      hosts:
        ml-api-01:
          ansible_host: 192.168.1.20
          api_port: 8000
        ml-api-02:
          ansible_host: 192.168.1.21
          api_port: 8000
      vars:
        max_workers: 4
    
    monitoring:
      hosts:
        prometheus:
          ansible_host: 192.168.1.30
        grafana:
          ansible_host: 192.168.1.31
    
  vars:
    ansible_user: ubuntu
    ansible_ssh_private_key_file: ~/.ssh/id_rsa
    ansible_python_interpreter: /usr/bin/python3
```

### Dynamic Inventory (AWS)
```python
#!/usr/bin/env python3
# inventory/aws_dynamic_inventory.py

import json
import boto3

def get_inventory():
    ec2 = boto3.client('ec2', region_name='us-east-1')
    
    response = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Environment', 'Values': ['mlops']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    
    inventory = {
        '_meta': {'hostvars': {}},
        'mlops_servers': {'hosts': []},
        'api_servers': {'hosts': []},
    }
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            hostname = instance['PrivateIpAddress']
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            
            # Add to appropriate group
            if 'Role' in tags:
                role = tags['Role']
                if role == 'training':
                    inventory['mlops_servers']['hosts'].append(hostname)
                elif role == 'api':
                    inventory['api_servers']['hosts'].append(hostname)
            
            # Add host vars
            inventory['_meta']['hostvars'][hostname] = {
                'ansible_host': hostname,
                'instance_id': instance['InstanceId'],
                'instance_type': instance['InstanceType'],
                'tags': tags
            }
    
    return inventory

if __name__ == '__main__':
    print(json.dumps(get_inventory(), indent=2))
```

### Inventory Commands
```bash
# List all hosts
ansible all --list-hosts

# List hosts in specific group
ansible mlops_servers --list-hosts

# View host variables
ansible-inventory --host ml-train-01

# List inventory in JSON format
ansible-inventory --list

# Verify inventory
ansible-inventory --graph

# Test connectivity
ansible all -m ping
ansible mlops_servers -m ping

# Use specific inventory file
ansible all -i inventory/production.yml --list-hosts
```

---

## Ad-Hoc Commands

### Basic Commands
```bash
# Ping all hosts
ansible all -m ping

# Check uptime
ansible all -m command -a "uptime"

# Get disk usage
ansible all -m shell -a "df -h"

# Check memory
ansible all -m shell -a "free -h"

# Install package
ansible all -m apt -a "name=htop state=present" --become

# Copy file
ansible all -m copy -a "src=/local/file dest=/remote/file"

# Create directory
ansible all -m file -a "path=/opt/mlops state=directory mode=0755" --become

# Restart service
ansible all -m systemd -a "name=nginx state=restarted" --become

# Gather facts
ansible all -m setup

# Filter facts
ansible all -m setup -a "filter=ansible_distribution*"
```

### File Operations
```bash
# Copy file to remote hosts
ansible mlops_servers -m copy -a "src=model.pkl dest=/opt/models/model.pkl"

# Template file
ansible all -m template -a "src=config.j2 dest=/etc/app/config.yml"

# Download file from remote
ansible ml-train-01 -m fetch -a "src=/remote/file.txt dest=/local/dir/"

# Change file permissions
ansible all -m file -a "path=/opt/app/script.sh mode=0755"

# Create symbolic link
ansible all -m file -a "src=/opt/app dest=/usr/local/bin/app state=link"

# Remove file
ansible all -m file -a "path=/tmp/old_file state=absent"
```

### Package Management
```bash
# Install package (apt)
ansible all -m apt -a "name=docker.io state=present update_cache=yes" --become

# Install multiple packages
ansible all -m apt -a "name=htop,vim,curl state=present" --become

# Upgrade all packages
ansible all -m apt -a "upgrade=dist" --become

# Remove package
ansible all -m apt -a "name=package_name state=absent" --become

# Install package (yum)
ansible all -m yum -a "name=nginx state=present" --become

# Install from pip
ansible all -m pip -a "name=mlflow state=present"
```

### Service Management
```bash
# Start service
ansible all -m systemd -a "name=nginx state=started" --become

# Stop service
ansible all -m systemd -a "name=nginx state=stopped" --become

# Restart service
ansible all -m systemd -a "name=nginx state=restarted" --become

# Enable service
ansible all -m systemd -a "name=nginx enabled=yes" --become

# Check service status
ansible all -m shell -a "systemctl status nginx"
```

### User Management
```bash
# Create user
ansible all -m user -a "name=mlops shell=/bin/bash" --become

# Add SSH key
ansible all -m authorized_key -a "user=mlops key='{{ lookup('file', '~/.ssh/id_rsa.pub') }}'" --become

# Add user to group
ansible all -m user -a "name=mlops groups=docker append=yes" --become

# Remove user
ansible all -m user -a "name=olduser state=absent remove=yes" --become
```

---

## Playbooks

### Basic Playbook Structure
```yaml
# playbooks/basic.yml
---
- name: Basic playbook example
  hosts: all
  become: yes
  
  vars:
    package_name: htop
  
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install package
      apt:
        name: "{{ package_name }}"
        state: present
    
    - name: Ensure service is running
      systemd:
        name: ssh
        state: started
        enabled: yes
```

### MLOps Setup Playbook
```yaml
# playbooks/mlops-setup.yml
---
- name: Setup MLOps Infrastructure
  hosts: mlops_servers
  become: yes
  
  vars:
    python_version: "3.11"
    docker_compose_version: "2.23.0"
    mlflow_version: "2.8.1"
    
  tasks:
    - name: Update system packages
      apt:
        update_cache: yes
        upgrade: dist
        cache_valid_time: 3600
    
    - name: Install system dependencies
      apt:
        name:
          - python3-pip
          - python3-venv
          - git
          - curl
          - wget
          - build-essential
          - libssl-dev
          - ca-certificates
          - gnupg
          - lsb-release
        state: present
    
    - name: Create keyring directory
      file:
        path: /etc/apt/keyrings
        state: directory
        mode: '0755'
    
    - name: Add Docker GPG key
      get_url:
        url: https://download.docker.com/linux/ubuntu/gpg
        dest: /etc/apt/keyrings/docker.asc
        mode: '0644'
    
    - name: Add Docker repository
      apt_repository:
        repo: "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"
        state: present
    
    - name: Install Docker
      apt:
        name:
          - docker-ce
          - docker-ce-cli
          - containerd.io
          - docker-buildx-plugin
          - docker-compose-plugin
        state: present
        update_cache: yes
    
    - name: Add user to docker group
      user:
        name: "{{ ansible_user }}"
        groups: docker
        append: yes
    
    - name: Start and enable Docker
      systemd:
        name: docker
        state: started
        enabled: yes
    
    - name: Install Python packages
      pip:
        name:
          - mlflow=={{ mlflow_version }}
          - dvc
          - boto3
          - pandas
          - scikit-learn
          - jupyter
        state: present
        executable: pip3
    
    - name: Create MLOps directories
      file:
        path: "{{ item }}"
        state: directory
        mode: '0755'
        owner: "{{ ansible_user }}"
      loop:
        - /opt/mlops
        - /opt/mlops/data
        - /opt/mlops/models
        - /opt/mlops/logs
    
    - name: Copy MLflow configuration
      template:
        src: templates/mlflow_config.yml.j2
        dest: /opt/mlops/mlflow_config.yml
        mode: '0644'
    
    - name: Create systemd service for MLflow
      template:
        src: templates/mlflow.service.j2
        dest: /etc/systemd/system/mlflow.service
        mode: '0644'
      notify: restart mlflow
  
  handlers:
    - name: restart mlflow
      systemd:
        name: mlflow
        state: restarted
        daemon_reload: yes
        enabled: yes
```

### Docker Deployment Playbook
```yaml
# playbooks/deploy-docker-app.yml
---
- name: Deploy ML API with Docker
  hosts: api_servers
  become: yes
  
  vars:
    app_name: ml-api
    image_name: "my-registry/ml-api"
    image_tag: "{{ lookup('env', 'IMAGE_TAG') | default('latest', true) }}"
    container_port: 8000
    host_port: 8000
    
  tasks:
    - name: Login to Docker registry
      docker_login:
        registry_url: "{{ docker_registry }}"
        username: "{{ docker_username }}"
        password: "{{ docker_password }}"
      no_log: yes
    
    - name: Pull Docker image
      docker_image:
        name: "{{ image_name }}"
        tag: "{{ image_tag }}"
        source: pull
        force_source: yes
    
    - name: Stop existing container
      docker_container:
        name: "{{ app_name }}"
        state: absent
      ignore_errors: yes
    
    - name: Start new container
      docker_container:
        name: "{{ app_name }}"
        image: "{{ image_name }}:{{ image_tag }}"
        state: started
        restart_policy: always
        ports:
          - "{{ host_port }}:{{ container_port }}"
        env:
          MLFLOW_TRACKING_URI: "{{ mlflow_uri }}"
          MODEL_VERSION: "{{ model_version }}"
        volumes:
          - /opt/mlops/logs:/app/logs
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
          interval: 30s
          timeout: 10s
          retries: 3
          start_period: 40s
    
    - name: Wait for container to be healthy
      wait_for:
        host: localhost
        port: "{{ host_port }}"
        delay: 5
        timeout: 60
    
    - name: Verify API health
      uri:
        url: "http://localhost:{{ host_port }}/health"
        method: GET
        status_code: 200
      register: health_check
      retries: 5
      delay: 10
    
    - name: Display deployment info
      debug:
        msg: "Successfully deployed {{ app_name }} version {{ image_tag }}"
```

### Kubernetes Deployment Playbook
```yaml
# playbooks/deploy-k8s.yml
---
- name: Deploy ML Application to Kubernetes
  hosts: localhost
  connection: local
  
  vars:
    namespace: mlops
    app_name: ml-api
    image_tag: "{{ lookup('env', 'IMAGE_TAG') | default('latest', true) }}"
    replicas: 3
    
  tasks:
    - name: Create namespace
      k8s:
        state: present
        definition:
          apiVersion: v1
          kind: Namespace
          metadata:
            name: "{{ namespace }}"
    
    - name: Create ConfigMap
      k8s:
        state: present
        definition:
          apiVersion: v1
          kind: ConfigMap
          metadata:
            name: "{{ app_name }}-config"
            namespace: "{{ namespace }}"
          data:
            MLFLOW_TRACKING_URI: "http://mlflow.mlops.svc.cluster.local:5000"
            LOG_LEVEL: "INFO"
    
    - name: Create Secret
      k8s:
        state: present
        definition:
          apiVersion: v1
          kind: Secret
          metadata:
            name: "{{ app_name }}-secret"
            namespace: "{{ namespace }}"
          type: Opaque
          stringData:
            AWS_ACCESS_KEY_ID: "{{ aws_access_key }}"
            AWS_SECRET_ACCESS_KEY: "{{ aws_secret_key }}"
      no_log: yes
    
    - name: Deploy application
      k8s:
        state: present
        definition:
          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: "{{ app_name }}"
            namespace: "{{ namespace }}"
          spec:
            replicas: "{{ replicas }}"
            selector:
              matchLabels:
                app: "{{ app_name }}"
            template:
              metadata:
                labels:
                  app: "{{ app_name }}"
              spec:
                containers:
                  - name: "{{ app_name }}"
                    image: "my-registry/{{ app_name }}:{{ image_tag }}"
                    ports:
                      - containerPort: 8000
                    envFrom:
                      - configMapRef:
                          name: "{{ app_name }}-config"
                      - secretRef:
                          name: "{{ app_name }}-secret"
                    resources:
                      requests:
                        memory: "512Mi"
                        cpu: "250m"
                      limits:
                        memory: "1Gi"
                        cpu: "500m"
                    livenessProbe:
                      httpGet:
                        path: /health
                        port: 8000
                      initialDelaySeconds: 30
                      periodSeconds: 10
                    readinessProbe:
                      httpGet:
                        path: /health
                        port: 8000
                      initialDelaySeconds: 5
                      periodSeconds: 5
    
    - name: Create Service
      k8s:
        state: present
        definition:
          apiVersion: v1
          kind: Service
          metadata:
            name: "{{ app_name }}"
            namespace: "{{ namespace }}"
          spec:
            type: LoadBalancer
            selector:
              app: "{{ app_name }}"
            ports:
              - port: 80
                targetPort: 8000
                protocol: TCP
    
    - name: Wait for deployment rollout
      shell: |
        kubectl rollout status deployment/{{ app_name }} -n {{ namespace }} --timeout=5m
```

---

## Roles

### Role Structure
```bash
# Create role
ansible-galaxy init ml-training-server

# Role directory structure
roles/ml-training-server/
├── defaults/
│   └── main.yml        # Default variables
├── files/              # Static files to copy
├── handlers/
│   └── main.yml        # Handlers (triggered by notify)
├── meta/
│   └── main.yml        # Role metadata and dependencies
├── tasks/
│   └── main.yml        # Main task list
├── templates/          # Jinja2 templates
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/
    └── main.yml        # Role variables
```

### Example Role: ML Training Server
```yaml
# roles/ml-training-server/tasks/main.yml
---
- name: Update apt cache
  apt:
    update_cache: yes
    cache_valid_time: 3600

- name: Install system packages
  apt:
    name:
      - python3-pip
      - python3-venv
      - git
      - nvidia-cuda-toolkit
    state: present

- name: Install Python packages
  pip:
    name:
      - torch
      - tensorflow
      - transformers
      - mlflow
      - dvc
    state: present

- name: Create training directory
  file:
    path: /opt/training
    state: directory
    mode: '0755'
    owner: "{{ ansible_user }}"

- name: Copy training scripts
  copy:
    src: "{{ item }}"
    dest: /opt/training/
    mode: '0755'
  loop:
    - train.py
    - evaluate.py
    - utils.py

- name: Create systemd service
  template:
    src: training.service.j2
    dest: /etc/systemd/system/training.service
  notify: restart training service
```

```yaml
# roles/ml-training-server/handlers/main.yml
---
- name: restart training service
  systemd:
    name: training
    state: restarted
    daemon_reload: yes
    enabled: yes
```

```yaml
# roles/ml-training-server/defaults/main.yml
---
python_version: "3.11"
cuda_version: "11.8"
training_dir: /opt/training
```

### Using Roles in Playbook
```yaml
# playbooks/setup-training-servers.yml
---
- name: Setup ML Training Servers
  hosts: mlops_servers
  become: yes
  
  roles:
    - common
    - docker
    - ml-training-server
    - monitoring-agent
  
  post_tasks:
    - name: Verify setup
      command: nvidia-smi
      register: nvidia_output
    
    - name: Display GPU info
      debug:
        var: nvidia_output.stdout_lines
```

---

## Jinja2 Templates

### Basic Template
```jinja2
{# templates/mlflow_config.yml.j2 #}
mlflow:
  tracking_uri: {{ mlflow_tracking_uri }}
  experiment_name: {{ experiment_name }}
  artifact_location: {{ artifact_location }}

storage:
  backend: {{ storage_backend }}
  {% if storage_backend == 's3' %}
  s3_bucket: {{ s3_bucket }}
  region: {{ aws_region }}
  {% elif storage_backend == 'local' %}
  path: {{ local_storage_path }}
  {% endif %}

logging:
  level: {{ log_level | default('INFO') }}
  file: {{ log_file | default('/var/log/mlflow.log') }}
```

### Nginx Configuration Template
```jinja2
{# templates/nginx-ml-api.conf.j2 #}
upstream ml_api {
    {% for host in groups['api_servers'] %}
    server {{ hostvars[host]['ansible_host'] }}:{{ api_port }};
    {% endfor %}
}

server {
    listen 80;
    server_name {{ server_name }};

    location / {
        proxy_pass http://ml_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts for ML inference
        proxy_connect_timeout {{ proxy_timeout }}s;
        proxy_send_timeout {{ proxy_timeout }}s;
        proxy_read_timeout {{ proxy_timeout }}s;
    }
    
    location /health {
        access_log off;
        proxy_pass http://ml_api/health;
    }
}
```

### Docker Compose Template
```jinja2
{# templates/docker-compose.yml.j2 #}
version: '3.8'

services:
  mlflow:
    image: mlflow:{{ mlflow_version }}
    ports:
      - "{{ mlflow_port }}:5000"
    environment:
      - BACKEND_STORE_URI={{ backend_store_uri }}
      - DEFAULT_ARTIFACT_ROOT={{ artifact_root }}
    volumes:
      - mlflow_data:/mlflow
    restart: always

  ml-api:
    image: {{ registry }}/ml-api:{{ image_tag }}
    ports:
      - "{{ api_port }}:8000"
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000
      - MODEL_VERSION={{ model_version }}
      - WORKERS={{ workers }}
    depends_on:
      - mlflow
    restart: always
    deploy:
      replicas: {{ api_replicas }}
      resources:
        limits:
          cpus: '{{ cpu_limit }}'
          memory: {{ memory_limit }}

volumes:
  mlflow_data:
```

---

## Variables & Facts

### Variable Precedence (Highest to Lowest)
```yaml
1. Extra vars (-e in CLI)
2. Task vars
3. Block vars
4. Role and include vars
5. Set_facts
6. Registered vars
7. Play vars_files
8. Play vars_prompt
9. Play vars
10. Host facts
11. Playbook host_vars
12. Playbook group_vars
13. Inventory host_vars
14. Inventory group_vars
15. Role defaults
```

### Using Variables
```yaml
---
- name: Variable examples
  hosts: all
  
  vars:
    app_name: ml-api
    app_version: 1.0.0
    
  vars_files:
    - vars/common.yml
    - vars/{{ environment }}.yml
    
  tasks:
    - name: Set variable dynamically
      set_fact:
        deployment_time: "{{ ansible_date_time.iso8601 }}"
    
    - name: Use variables
      debug:
        msg: "Deploying {{ app_name }} version {{ app_version }} at {{ deployment_time }}"
    
    - name: Register command output
      command: df -h /
      register: disk_usage
    
    - name: Use registered variable
      debug:
        var: disk_usage.stdout_lines
```

### Gathering Facts
```yaml
---
- name: Fact gathering examples
  hosts: all
  gather_facts: yes
  
  tasks:
    - name: Display OS info
      debug:
        msg: "OS: {{ ansible_distribution }} {{ ansible_distribution_version }}"
    
    - name: Display memory
      debug:
        msg: "Total memory: {{ ansible_memtotal_mb }} MB"
    
    - name: Display CPU count
      debug:
        msg: "CPU cores: {{ ansible_processor_vcpus }}"
    
    - name: Custom facts
      set_fact:
        is_gpu_server: "{{ 'nvidia' in ansible_kernel | lower }}"
    
    - name: Use custom fact
      debug:
        msg: "GPU server: {{ is_gpu_server }}"
```

---

## Conditionals & Loops

### Conditionals
```yaml
---
- name: Conditional examples
  hosts: all
  
  tasks:
    - name: Install package on Ubuntu
      apt:
        name: nginx
        state: present
      when: ansible_distribution == "Ubuntu"
    
    - name: Install package on CentOS
      yum:
        name: nginx
        state: present
      when: ansible_distribution == "CentOS"
    
    - name: Install GPU drivers
      apt:
        name: nvidia-driver
        state: present
      when:
        - gpu_enabled is defined
        - gpu_enabled | bool
        - ansible_distribution == "Ubuntu"
    
    - name: Multiple conditions
      debug:
        msg: "This is a production GPU server"
      when:
        - environment == "production"
        - ansible_processor_vcpus >= 8
        - ansible_memtotal_mb >= 16384
```

### Loops
```yaml
---
- name: Loop examples
  hosts: all
  
  tasks:
    - name: Install multiple packages
      apt:
        name: "{{ item }}"
        state: present
      loop:
        - vim
        - git
        - curl
        - htop
    
    - name: Create multiple directories
      file:
        path: "{{ item.path }}"
        state: directory
        mode: "{{ item.mode }}"
      loop:
        - { path: '/opt/mlops/data', mode: '0755' }
        - { path: '/opt/mlops/models', mode: '0755' }
        - { path: '/opt/mlops/logs', mode: '0775' }
    
    - name: Loop over dictionary
      debug:
        msg: "{{ item.key }} = {{ item.value }}"
      loop: "{{ mlflow_config | dict2items }}"
      vars:
        mlflow_config:
          tracking_uri: http://mlflow:5000
          experiment_name: production
          artifact_location: s3://mlops-artifacts
    
    - name: Loop with index
      debug:
        msg: "Server {{ ansible_loop.index }}: {{ item }}"
      loop: "{{ groups['api_servers'] }}"
      loop_control:
        loop_var: item
```

---

## Real-Time MLOps Scenarios

### Scenario 1: Automated ML Environment Setup
```yaml
# playbooks/setup-ml-environment.yml
---
- name: Setup Complete ML Environment
  hosts: ml_servers
  become: yes
  
  vars:
    python_version: "3.11"
    cuda_version: "11.8"
    workspace_dir: /opt/ml-workspace
    
  tasks:
    - name: Update system
      apt:
        update_cache: yes
        upgrade: dist
    
    - name: Install system dependencies
      apt:
        name:
          - build-essential
          - python3-dev
          - python3-pip
          - git
          - curl
          - wget
        state: present
    
    - name: Install NVIDIA drivers (if GPU server)
      block:
        - name: Add NVIDIA repository
          apt_repository:
            repo: ppa:graphics-drivers/ppa
            state: present
        
        - name: Install NVIDIA driver
          apt:
            name: nvidia-driver-535
            state: present
        
        - name: Install CUDA toolkit
          apt:
            name: nvidia-cuda-toolkit
            state: present
      when: gpu_enabled | default(false)
    
    - name: Install Docker
      include_role:
        name: docker
    
    - name: Create workspace structure
      file:
        path: "{{ item }}"
        state: directory
        mode: '0755'
        owner: "{{ ansible_user }}"
      loop:
        - "{{ workspace_dir }}"
        - "{{ workspace_dir }}/data"
        - "{{ workspace_dir }}/models"
        - "{{ workspace_dir }}/notebooks"
        - "{{ workspace_dir }}/scripts"
        - "{{ workspace_dir }}/logs"
    
    - name: Install Python ML packages
      pip:
        name:
          - numpy
          - pandas
          - scikit-learn
          - torch
          - tensorflow
          - mlflow
          - dvc
          - jupyter
          - matplotlib
          - seaborn
        state: present
        executable: pip3
    
    - name: Setup Jupyter Lab
      block:
        - name: Generate Jupyter config
          command: jupyter lab --generate-config
          become_user: "{{ ansible_user }}"
        
        - name: Configure Jupyter Lab
          lineinfile:
            path: /home/{{ ansible_user }}/.jupyter/jupyter_lab_config.py
            line: "{{ item }}"
            create: yes
          loop:
            - "c.ServerApp.ip = '0.0.0.0'"
            - "c.ServerApp.port = 8888"
            - "c.ServerApp.open_browser = False"
            - "c.ServerApp.root_dir = '{{ workspace_dir }}/notebooks'"
        
        - name: Create Jupyter systemd service
          template:
            src: templates/jupyter.service.j2
            dest: /etc/systemd/system/jupyter.service
          notify: restart jupyter
    
    - name: Setup DVC
      block:
        - name: Initialize DVC
          command: dvc init
          args:
            chdir: "{{ workspace_dir }}"
            creates: "{{ workspace_dir }}/.dvc"
          become_user: "{{ ansible_user }}"
        
        - name: Configure DVC remote
          command: dvc remote add -d storage s3://ml-data-bucket
          args:
            chdir: "{{ workspace_dir }}"
          become_user: "{{ ansible_user }}"
    
    - name: Setup MLflow
      docker_container:
        name: mlflow
        image: mlflow:latest
        state: started
        restart_policy: always
        ports:
          - "5000:5000"
        volumes:
          - mlflow_data:/mlflow
        env:
          BACKEND_STORE_URI: sqlite:///mlflow/mlflow.db
          DEFAULT_ARTIFACT_ROOT: /mlflow/artifacts
  
  handlers:
    - name: restart jupyter
      systemd:
        name: jupyter
        state: restarted
        enabled: yes
        daemon_reload: yes
```

### Scenario 2: Model Deployment Pipeline
```yaml
# playbooks/deploy-model.yml
---
- name: Deploy ML Model to Production
  hosts: api_servers
  become: yes
  serial: 1  # Rolling deployment
  
  vars:
    model_name: churn_predictor
    model_version: "{{ lookup('env', 'MODEL_VERSION') }}"
    healthcheck_retries: 5
    healthcheck_delay: 10
    
  pre_tasks:
    - name: Verify model version provided
      fail:
        msg: "MODEL_VERSION environment variable not set"
      when: model_version == ""
    
    - name: Check current deployment
      uri:
        url: http://localhost:8000/health
        method: GET
        status_code: 200
      register: current_health
      failed_when: false
  
  tasks:
    - name: Download model from MLflow
      block:
        - name: Create temp directory
          file:
            path: /tmp/model_download
            state: directory
        
        - name: Download model artifacts
          command: >
            mlflow artifacts download
            --run-id {{ model_version }}
            --artifact-path model
            --dst-path /tmp/model_download
          environment:
            MLFLOW_TRACKING_URI: "{{ mlflow_uri }}"
        
        - name: Copy model to deployment directory
          copy:
            src: /tmp/model_download/model/
            dest: /opt/models/{{ model_name }}/{{ model_version }}/
            remote_src: yes
    
    - name: Update API configuration
      template:
        src: templates/api_config.yml.j2
        dest: /opt/ml-api/config.yml
        backup: yes
      notify: restart api
    
    - name: Update symlink to new model
      file:
        src: /opt/models/{{ model_name }}/{{ model_version }}
        dest: /opt/models/{{ model_name }}/current
        state: link
      notify: restart api
    
    - name: Flush handlers
      meta: flush_handlers
    
    - name: Wait for API to be ready
      wait_for:
        host: localhost
        port: 8000
        delay: 5
        timeout: 60
    
    - name: Health check
      uri:
        url: http://localhost:8000/health
        method: GET
        status_code: 200
      register: health_result
      retries: "{{ healthcheck_retries }}"
      delay: "{{ healthcheck_delay }}"
      until: health_result.status == 200
    
    - name: Run smoke tests
      script: scripts/smoke_test.sh http://localhost:8000
      register: smoke_test_result
    
    - name: Rollback on failure
      block:
        - name: Restore previous symlink
          file:
            src: /opt/models/{{ model_name }}/previous
            dest: /opt/models/{{ model_name }}/current
            state: link
        
        - name: Restart API with previous version
          systemd:
            name: ml-api
            state: restarted
        
        - name: Fail deployment
          fail:
            msg: "Deployment failed smoke tests, rolled back to previous version"
      when: smoke_test_result.rc != 0
    
    - name: Update previous version marker
      file:
        src: /opt/models/{{ model_name }}/{{ model_version }}
        dest: /opt/models/{{ model_name }}/previous
        state: link
      when: smoke_test_result.rc == 0
  
  handlers:
    - name: restart api
      systemd:
        name: ml-api
        state: restarted

- name: Update monitoring
  hosts: monitoring
  become: yes
  
  tasks:
    - name: Update Grafana annotation
      uri:
        url: http://localhost:3000/api/annotations
        method: POST
        user: admin
        password: "{{ grafana_password }}"
        body_format: json
        body:
          text: "Model {{ model_name }} version {{ model_version }} deployed"
          tags:
            - deployment
            - model
          time: "{{ ansible_date_time.epoch }}000"
        status_code: 200
```

### Scenario 3: Data Pipeline Management
```yaml
# playbooks/manage-data-pipeline.yml
---
- name: Manage ML Data Pipeline
  hosts: data_servers
  become: yes
  
  vars:
    pipeline_dir: /opt/data-pipeline
    dvc_remote: s3://ml-data-bucket
    
  tasks:
    - name: Ensure pipeline directory exists
      file:
        path: "{{ pipeline_dir }}"
        state: directory
        owner: "{{ ansible_user }}"
        mode: '0755'
    
    - name: Clone data pipeline repository
      git:
        repo: https://github.com/org/ml-data-pipeline.git
        dest: "{{ pipeline_dir }}"
        version: main
        force: yes
      become_user: "{{ ansible_user }}"
    
    - name: Install pipeline dependencies
      pip:
        requirements: "{{ pipeline_dir }}/requirements.txt"
        virtualenv: "{{ pipeline_dir }}/venv"
        virtualenv_command: python3 -m venv
    
    - name: Configure DVC remote
      command: dvc remote modify storage url {{ dvc_remote }}
      args:
        chdir: "{{ pipeline_dir }}"
      become_user: "{{ ansible_user }}"
    
    - name: Pull latest data
      command: dvc pull
      args:
        chdir: "{{ pipeline_dir }}"
      become_user: "{{ ansible_user }}"
      register: dvc_pull_result
    
    - name: Run data validation
      command: "{{ pipeline_dir }}/venv/bin/python scripts/validate_data.py"
      args:
        chdir: "{{ pipeline_dir }}"
      register: validation_result
    
    - name: Run data preprocessing
      command: "{{ pipeline_dir }}/venv/bin/python scripts/preprocess.py"
      args:
        chdir: "{{ pipeline_dir }}"
      when: validation_result.rc == 0
    
    - name: Push processed data to DVC
      block:
        - name: Add processed data to DVC
          command: dvc add data/processed
          args:
            chdir: "{{ pipeline_dir }}"
        
        - name: Push to DVC remote
          command: dvc push
          args:
            chdir: "{{ pipeline_dir }}"
        
        - name: Commit DVC files
          shell: |
            git add data/processed.dvc .gitignore
            git commit -m "Update processed data $(date +%Y%m%d)"
            git push origin main
          args:
            chdir: "{{ pipeline_dir }}"
      become_user: "{{ ansible_user }}"
      when: validation_result.rc == 0
    
    - name: Trigger training workflow
      uri:
        url: "{{ cicd_webhook_url }}"
        method: POST
        body_format: json
        body:
          ref: main
          inputs:
            dataset_version: "{{ lookup('pipe', 'git -C ' + pipeline_dir + ' rev-parse HEAD') }}"
        headers:
          Authorization: "Bearer {{ github_token }}"
        status_code: 204
      when: validation_result.rc == 0
```

### Scenario 4: Monitoring Stack Deployment
```yaml
# playbooks/deploy-monitoring.yml
---
- name: Deploy Monitoring Stack
  hosts: monitoring
  become: yes
  
  vars:
    prometheus_version: "2.47.0"
    grafana_version: "10.1.0"
    node_exporter_version: "1.6.1"
    
  tasks:
    - name: Create monitoring directories
      file:
        path: "{{ item }}"
        state: directory
        mode: '0755'
      loop:
        - /opt/monitoring
        - /opt/monitoring/prometheus
        - /opt/monitoring/grafana
        - /etc/prometheus
        - /var/lib/prometheus
    
    - name: Deploy Prometheus
      block:
        - name: Copy Prometheus configuration
          template:
            src: templates/prometheus.yml.j2
            dest: /etc/prometheus/prometheus.yml
          notify: restart prometheus
        
        - name: Copy alert rules
          copy:
            src: files/alert_rules.yml
            dest: /etc/prometheus/alert_rules.yml
          notify: restart prometheus
        
        - name: Create Prometheus container
          docker_container:
            name: prometheus
            image: prom/prometheus:v{{ prometheus_version }}
            state: started
            restart_policy: always
            ports:
              - "9090:9090"
            volumes:
              - /etc/prometheus:/etc/prometheus
              - /var/lib/prometheus:/prometheus
            command:
              - '--config.file=/etc/prometheus/prometheus.yml'
              - '--storage.tsdb.path=/prometheus'
              - '--web.console.libraries=/usr/share/prometheus/console_libraries'
              - '--web.console.templates=/usr/share/prometheus/consoles'
    
    - name: Deploy Grafana
      block:
        - name: Create Grafana container
          docker_container:
            name: grafana
            image: grafana/grafana:{{ grafana_version }}
            state: started
            restart_policy: always
            ports:
              - "3000:3000"
            volumes:
              - /opt/monitoring/grafana:/var/lib/grafana
            env:
              GF_SECURITY_ADMIN_PASSWORD: "{{ grafana_admin_password }}"
              GF_INSTALL_PLUGINS: "grafana-piechart-panel"
        
        - name: Wait for Grafana to start
          wait_for:
            host: localhost
            port: 3000
            delay: 5
            timeout: 30
        
        - name: Add Prometheus datasource
          uri:
            url: http://localhost:3000/api/datasources
            method: POST
            user: admin
            password: "{{ grafana_admin_password }}"
            body_format: json
            body:
              name: Prometheus
              type: prometheus
              url: http://prometheus:9090
              access: proxy
              isDefault: true
            status_code: [200, 409]
        
        - name: Import ML dashboards
          uri:
            url: http://localhost:3000/api/dashboards/db
            method: POST
            user: admin
            password: "{{ grafana_admin_password }}"
            body_format: json
            body: "{{ lookup('file', item) | from_json }}"
            status_code: 200
          loop:
            - files/dashboards/ml_api_dashboard.json
            - files/dashboards/model_performance_dashboard.json
  
  handlers:
    - name: restart prometheus
      docker_container:
        name: prometheus
        state: started
        restart: yes

- name: Deploy Node Exporter on all servers
  hosts: all
  become: yes
  
  tasks:
    - name: Download node_exporter
      get_url:
        url: "https://github.com/prometheus/node_exporter/releases/download/v{{ node_exporter_version }}/node_exporter-{{ node_exporter_version }}.linux-amd64.tar.gz"
        dest: /tmp/node_exporter.tar.gz
    
    - name: Extract node_exporter
      unarchive:
        src: /tmp/node_exporter.tar.gz
        dest: /tmp
        remote_src: yes
    
    - name: Copy node_exporter binary
      copy:
        src: "/tmp/node_exporter-{{ node_exporter_version }}.linux-amd64/node_exporter"
        dest: /usr/local/bin/node_exporter
        mode: '0755'
        remote_src: yes
    
    - name: Create node_exporter systemd service
      copy:
        content: |
          [Unit]
          Description=Node Exporter
          After=network.target

          [Service]
          Type=simple
          ExecStart=/usr/local/bin/node_exporter

          [Install]
          WantedBy=multi-user.target
        dest: /etc/systemd/system/node_exporter.service
      notify: restart node_exporter
  
  handlers:
    - name: restart node_exporter
      systemd:
        name: node_exporter
        state: restarted
        enabled: yes
        daemon_reload: yes
```

### Scenario 5: Disaster Recovery & Backup
```yaml
# playbooks/backup-restore.yml
---
- name: Backup ML Infrastructure
  hosts: all
  become: yes
  
  vars:
    backup_dir: /backup
    s3_bucket: s3://ml-backups
    timestamp: "{{ ansible_date_time.iso8601_basic_short }}"
    
  tasks:
    - name: Create backup directory
      file:
        path: "{{ backup_dir }}"
        state: directory
        mode: '0755'
    
    - name: Backup MLflow database
      block:
        - name: Dump MLflow database
          shell: |
            docker exec mlflow-db pg_dump -U mlflow mlflow > {{ backup_dir }}/mlflow_{{ timestamp }}.sql
          when: "'mlflow' in group_names"
        
        - name: Compress database backup
          archive:
            path: "{{ backup_dir }}/mlflow_{{ timestamp }}.sql"
            dest: "{{ backup_dir }}/mlflow_{{ timestamp }}.sql.gz"
            format: gz
            remove: yes
    
    - name: Backup models
      synchronize:
        src: /opt/models/
        dest: "{{ backup_dir }}/models_{{ timestamp }}/"
        mode: pull
      delegate_to: localhost
      when: "'api_servers' in group_names"
    
    - name: Backup configurations
      archive:
        path:
          - /opt/ml-api/config.yml
          - /etc/prometheus/prometheus.yml
          - /etc/nginx/sites-available/
        dest: "{{ backup_dir }}/configs_{{ timestamp }}.tar.gz"
        format: gz
    
    - name: Upload backups to S3
      aws_s3:
        bucket: ml-backups
        object: "{{ inventory_hostname }}/{{ item | basename }}"
        src: "{{ item }}"
        mode: put
      loop:
        - "{{ backup_dir }}/mlflow_{{ timestamp }}.sql.gz"
        - "{{ backup_dir }}/configs_{{ timestamp }}.tar.gz"
      when: backup_to_s3 | default(true)
    
    - name: Rotate old backups (keep last 7 days)
      find:
        paths: "{{ backup_dir }}"
        age: 7d
        file_type: file
      register: old_backups
    
    - name: Delete old backups
      file:
        path: "{{ item.path }}"
        state: absent
      loop: "{{ old_backups.files }}"

- name: Restore from Backup
  hosts: all
  become: yes
  
  vars:
    restore_version: latest
    backup_dir: /backup
    
  tasks:
    - name: Download backup from S3
      aws_s3:
        bucket: ml-backups
        object: "{{ inventory_hostname }}/{{ restore_file }}"
        dest: "{{ backup_dir }}/{{ restore_file }}"
        mode: get
      when: restore_from_s3 | default(false)
    
    - name: Restore MLflow database
      block:
        - name: Stop MLflow service
          systemd:
            name: mlflow
            state: stopped
        
        - name: Restore database
          shell: |
            gunzip -c {{ backup_dir }}/{{ restore_file }} | docker exec -i mlflow-db psql -U mlflow mlflow
        
        - name: Start MLflow service
          systemd:
            name: mlflow
            state: started
      when: "'mlflow' in group_names and restore_mlflow | default(false)"
    
    - name: Restore configurations
      unarchive:
        src: "{{ backup_dir }}/configs_{{ restore_version }}.tar.gz"
        dest: /
        remote_src: yes
      when: restore_configs | default(false)
```

---

## Ansible Vault (Secrets Management)

### Creating & Managing Vaults
```bash
# Create encrypted file
ansible-vault create secrets.yml

# Edit encrypted file
ansible-vault edit secrets.yml

# Encrypt existing file
ansible-vault encrypt vars/production.yml

# Decrypt file
ansible-vault decrypt vars/production.yml

# View encrypted file
ansible-vault view secrets.yml

# Change vault password
ansible-vault rekey secrets.yml

# Encrypt string
ansible-vault encrypt_string 'secret_password' --name 'db_password'
```

### Using Vault in Playbooks
```yaml
# vars/secrets.yml (encrypted)
---
aws_access_key: AKIA...
aws_secret_key: secret123
db_password: mydbpass
mlflow_admin_token: token123

# playbook.yml
---
- name: Deploy with secrets
  hosts: all
  vars_files:
    - vars/secrets.yml
  
  tasks:
    - name: Use secret
      debug:
        msg: "Database password: {{ db_password }}"
      no_log: yes
```

### Running with Vault
```bash
# Prompt for vault password
ansible-playbook playbook.yml --ask-vault-pass

# Use password file
ansible-playbook playbook.yml --vault-password-file ~/.vault_pass

# Multiple vault passwords
ansible-playbook playbook.yml --vault-id prod@~/.vault_pass_prod --vault-id dev@~/.vault_pass_dev
```

---

## Error Handling

### Error Handling Strategies
```yaml
---
- name: Error handling examples
  hosts: all
  
  tasks:
    - name: Task that might fail
      command: /bin/false
      ignore_errors: yes
    
    - name: Register and check result
      command: some_command
      register: result
      failed_when: result.rc != 0 and result.rc != 2
    
    - name: Handle specific errors
      block:
        - name: Risky task
          command: risky_operation
      rescue:
        - name: Handle failure
          debug:
            msg: "Task failed, running recovery"
        
        - name: Recovery task
          command: recovery_operation
      always:
        - name: Cleanup
          file:
            path: /tmp/temp_file
            state: absent
    
    - name: Retry task
      uri:
        url: http://api.example.com
        method: GET
      register: result
      until: result.status == 200
      retries: 5
      delay: 10
```

---

## Testing & Validation

### Ansible Lint
```bash
# Install ansible-lint
pip install ansible-lint

# Lint playbook
ansible-lint playbook.yml

# Lint all playbooks
ansible-lint playbooks/

# Custom rules
ansible-lint -r custom_rules/ playbook.yml
```

### Molecule (Role Testing)
```bash
# Install Molecule
pip install molecule molecule-docker

# Initialize Molecule in role
cd roles/my-role
molecule init scenario

# Test role
molecule test

# Create instance
molecule create

# Apply role
molecule converge

# Run tests
molecule verify

# Destroy instance
molecule destroy
```

### Playbook Syntax Check
```bash
# Check syntax
ansible-playbook --syntax-check playbook.yml

# Dry run
ansible-playbook --check playbook.yml

# Diff mode (show changes)
ansible-playbook --check --diff playbook.yml

# Step through playbook
ansible-playbook --step playbook.yml
```

---

## Performance Optimization

### Optimization Techniques
```yaml
---
- name: Optimized playbook
  hosts: all
  gather_facts: no  # Skip if not needed
  
  tasks:
    - name: Gather specific facts
      setup:
        gather_subset:
          - '!all'
          - '!min'
          - network
    
    - name: Run tasks in parallel
      command: "{{ item }}"
      loop:
        - task1
        - task2
        - task3
      async: 300
      poll: 0
      register: async_results
    
    - name: Wait for async tasks
      async_status:
        jid: "{{ item.ansible_job_id }}"
      loop: "{{ async_results.results }}"
      register: async_poll_results
      until: async_poll_results.finished
      retries: 30
      delay: 10

# ansible.cfg optimizations
[defaults]
forks = 50  # Increase parallelism
gathering = smart  # Smart fact caching
fact_caching = jsonfile
fact_caching_connection = /tmp/facts
pipelining = True  # Reduce SSH operations
```

### Mitogen Strategy Plugin (10x faster)
```bash
# Install Mitogen
pip install mitogen

# ansible.cfg
[defaults]
strategy_plugins = /path/to/mitogen/ansible_mitogen/plugins/strategy
strategy = mitogen_linear

# Use in playbook
---
- name: Fast playbook with Mitogen
  hosts: all
  strategy: mitogen_linear
```

---

## Best Practices

### Directory Structure
```
ansible/
├── ansible.cfg
├── inventory/
│   ├── production/
│   │   ├── hosts.yml
│   │   └── group_vars/
│   └── staging/
│       ├── hosts.yml
│       └── group_vars/
├── playbooks/
│   ├── site.yml
│   ├── deploy.yml
│   └── backup.yml
├── roles/
│   ├── common/
│   ├── docker/
│   ├── ml-api/
│   └── monitoring/
├── group_vars/
│   ├── all.yml
│   └── mlops_servers.yml
├── host_vars/
├── files/
├── templates/
├── library/          # Custom modules
└── filter_plugins/   # Custom filters
```

### Naming Conventions
```yaml
# Good naming
- name: Install Docker CE
- name: Copy API configuration
- name: Restart ML API service

# Bad naming
- name: install stuff
- name: do things
- name: task 1
```

### Idempotency
```yaml
# Always aim for idempotent tasks
- name: Ensure directory exists
  file:
    path: /opt/app
    state: directory  # Idempotent

# Not idempotent
- name: Create directory
  command: mkdir /opt/app  # Fails if exists
```

---

## Troubleshooting

### Common Issues

#### Connection Issues
```bash
# Test connectivity
ansible all -m ping -vvv

# Check SSH
ssh -i ~/.ssh/key.pem user@host

# Use different SSH key
ansible all -m ping --private-key=~/.ssh/other_key.pem

# Disable host key checking
export ANSIBLE_HOST_KEY_CHECKING=False
```

#### Permission Issues
```bash
# Become (sudo)
ansible all -m command -a "whoami" --become

# Become specific user
ansible all -m command -a "whoami" --become --become-user=root

# Ask for become password
ansible all -m command -a "whoami" --become --ask-become-pass
```

#### Debugging
```bash
# Verbose output
ansible-playbook playbook.yml -v    # verbose
ansible-playbook playbook.yml -vv   # more verbose
ansible-playbook playbook.yml -vvv  # very verbose
ansible-playbook playbook.yml -vvvv # connection debugging

# Debug tasks
- name: Debug variable
  debug:
    var: my_variable
    verbosity: 2  # Only show with -vv

# Playbook debugger
- name: Task to debug
  command: might_fail
  debugger: on_failed
```

---

## Resources

### Official Documentation
- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Galaxy](https://galaxy.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)

### Tools & Extensions
- [Ansible Lint](https://github.com/ansible/ansible-lint)
- [Molecule](https://molecule.readthedocs.io/)
- [Mitogen](https://mitogen.networkgenomics.com/ansible_detailed.html)
- [AWX](https://github.com/ansible/awx) - Web UI for Ansible

### Learning Resources
- [Ansible for DevOps Book](https://www.ansiblefordevops.com/)
- [Ansible 101 YouTube Series](https://www.youtube.com/playlist?list=PL2_OBreMn7FqZkvMYt6ATmgC0KAGGJNAN)

---

**[Back to Main Cheatsheets](../README.md)**

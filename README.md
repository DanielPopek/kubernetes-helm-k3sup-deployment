# Kubernetes deployment of distributed twitter scrapper

The goal of the project was to deploy to twitter scrapper from cellery-prometheus-twitter-scraper repo to Kubernetes clusters on AWS. 
K3sup and helm charts were used

## Subtasks
1. **Infrastructure setup**

    - create at least 3 EC2 machines with Ubuntu 18.04 
    - one machine will act as the Kubernetes master, the other ones will be worker nodes

2. **K3s cluster installation**

3. **Kubernetes objects & manifests with helm**

4. **Application chart**

    -  Docker images for our Twitter Scraper application - for all custom images (celery workers, scheduler etc.):
        - pushed as public images on your Docker Hub
    - create a Helm chart for application
    - write appropriate Helm templates (deployments, services, etc.) 
    - handle volumes! (hostPaths)

6. **Application deployment**
    - deploy the prepared application chart to your Kubernetes cluster
    - check if everything works fine
    - make some change in the `values.yaml`
    - rollback the change



# Django and NGINX Load Balanced Setup with Docker Compose

This project sets up a Django application with load balancing using NGINX and Docker Compose. The configuration runs two instances of the Django application and uses NGINX to balance the incoming requests between them.

## Goal

The goal of this project is to practice the use of NGINX and Docker Compose for setting up multiple applications services being served behind a Load Balancer. My desire is to develop the skills required to put in production some personal projects and apply these knowledge in my current job.

## Components

1. **Django Application**:
   - The Django application is built from a `Dockerfile`.
   - Two instances of the Django application are run in separate containers (`django1` and `django2`).

2. **NGINX**:
   - NGINX is used as a reverse proxy to balance the requests between the two Django instances.
   - Configuration is provided in the `nginx/nginx.conf` file.

3. **Docker Compose**:
   - `docker-compose.yml` is used to define and manage the multi-container setup.
   - It builds the Docker images, sets up the network, and runs the containers.

## Project Structure

```
.
├── api
│   ├── core
│   │   ├── middleware.py
│   │   ├── ...
│   ├── api
│   │   ├── settings.py
│   │   ├── ...
│   ├── Dockerfile
│   ├── requirements.txt
├── nginx.conf
├── docker-compose.yml
└── README.md
```

## Setting Up the Project

### Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

### Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/MicaelTargino/NGINX-LoadBalancer.git nginx-lb
   cd nginx-lb
   ```

2. **Build and run the containers**:

   ```bash
   docker-compose up --build
   ```

3. **Access the application**:

   Open your browser and navigate to `http://localhost`. NGINX will balance the requests between the two Django instances.

### Configuration Details

1. **Dockerfile**:

   The `Dockerfile` sets up the Django application, installs dependencies, and runs the application using Gunicorn.

2. **nginx.conf**:

   NGINX configuration to balance the requests between `django1` and `django2` instances.

   ```nginx
    events {}

    http {
        upstream django {
            server django1:8000;
            server django2:8000;
        }

        server {
            listen 80;

            location / {
                proxy_pass http://django;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
            }
        }
    }
   ```

3. **docker-compose.yml**:

   Defines the multi-container setup with two Django instances and one NGINX instance.

   ```yaml
  version: '3'

  services:
    django1:
      build:
        context: ./api/
        dockerfile: Dockerfile
      environment:
        - DJANGO_SETTINGS_MODULE=api.settings
        - INSTANCE=1
      networks:
        - mynetwork
      ports:
        - 8001:8000

    django2:
      build:
        context: ./api/
        dockerfile: Dockerfile
      environment:
        - DJANGO_SETTINGS_MODULE=api.settings
        - INSTANCE=2
      networks:
        - mynetwork
      ports:
        - 8002:8000    
      

    nginx:
      image: nginx:latest
      container_name: nginx
      ports:
        - "80:80"
      volumes:
        - ./nginx/default.conf:/etc/nginx/nginx.conf
      depends_on:
        - django1
        - django2
      networks:
        - mynetwork

  networks:
    mynetwork:
      driver: bridge
   ```

### Verifying the Setup

To verify which Django instance handled a request, see the Browser's response or inspect the response headers. Each instance answers a Json with the instance number (1 or 2) and the response includes an `X-Instance-Number` header indicating which instance served the request.

- visit `http://localhost`


You should see a response in the browser like `{"instance": "1"}` or `{"instance: "2"}` and a header like `X-Instance-Number: 1` or `X-Instance-Number: 2`.

## Troubleshooting

- Ensure Docker and Docker Compose are installed and running correctly.
- Check the logs for any errors by running `docker-compose logs`.
- Verify that the ports specified in the `docker-compose.yml` file are not being used by other services.

## Conclusion

This setup ensures a scalable and load-balanced Django application using Docker Compose and NGINX. By following the steps above, you can easily run and manage multiple instances of your Django application with load balancing.

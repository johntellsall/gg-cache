# gg-cache

# Deployment

Deployment happens in three phases:
- local "make deploy" runs, pushing code to GitHub
- Drone builds a Docker image from updated code, pushing image to DockerHub
- Heroku notices new Docker image, deploys it, and runs updated code
  
# Resources


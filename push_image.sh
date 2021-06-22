cd aiTrainer
docker build -f Dockerfile --pull -t docker-registry.ge-healthcare.com/visualizer.ge-healthcare.com:0.0.1 .
ID="$(docker images | grep 'docker-registry.ge-healthcare.com/visualizer.ge-healthcare.com' | head -n 1 | awk '{print $3}')"
docker tag "$ID" docker-registry.ge-healthcare.com/visualizer.ge-healthcare.com:0.0.1
docker tag "$ID" docker-registry.ge-healthcare.com/visualizer.ge-healthcare.com:latest
docker push docker-registry.ge-healthcare.com/visualizer.ge-healthcare.com:latest
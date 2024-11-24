SPARK_IMAGE=spark-image
APP_SPARK=./services/spark

CLUSTER_NAME=trading-term-cluster

build: 
	@echo "Building Docker images..."
	docker build -t $(SPARK_IMAGE) $(APP_SPARK)

apply:
	@echo "Create k8s cluster..."
	kind create cluster --name $(CLUSTER_NAME) --config ./k8s/kind-config.yaml
	@echo "Applying all resources to the cluster..."
	helm install spark-operator spark-operator/spark-operator --namespace spark-operator --create-namespace --wait
	kubectl apply -k $(APP_SPARK)

delete:
	@echo "Deleting k8s cluster..."
	kind delete cluster --name $(CLUSTER_NAME)

verify:
	@echo "Verifying deployments..."
	kubectl get pods

clean:
	@echo "Removing Docker images..."
	docker rmi $(SPARK_IMAGE)

.PHONY: build apply delete verify clean

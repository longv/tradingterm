SPARK=./services/spark
MONGO = ./services/mongo

CLUSTER_NAME=trading-term-cluster

setup:
	@echo "Adding Helm repos..."
	helm repo add mongodb https://mongodb.github.io/helm-charts

apply:
	@echo "Creating k8s cluster..."
	kind create cluster --name $(CLUSTER_NAME) --config kind-config.yaml
	@echo "Applying all resources to the cluster..."
	helm install spark-operator spark-operator/spark-operator --namespace spark-operator --create-namespace --wait
	kubectl apply -k $(SPARK)
	helm install community-operator mongodb/community-operator --namespace mongodb --create-namespace --wait
	kubectl apply -f $(MONGO)/mongodb.yaml

update:
	@echo "Re-applying all resources to the cluster..."
	kubectl apply -k $(SPARK)

delete:
	@echo "Deleting k8s cluster..."
	kind delete cluster --name $(CLUSTER_NAME)

verify:
	@echo "Verifying deployments in default namespace..."
	kubectl get pods

verify/spark:
	@echo "Verifying deployments in spark-operator namespace..."
	kubectl get pods -n spark-operator

verify/mongo:
	@echo "Verifying deployments in mongodb namespace..."
	kubectl get pods -n mongodb

.PHONY: apply delete verify verify/operator

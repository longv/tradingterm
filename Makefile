APP_SPARK=./services/spark

CLUSTER_NAME=trading-term-cluster

apply:
	@echo "Create k8s cluster..."
	kind create cluster --name $(CLUSTER_NAME) --config kind-config.yaml
	@echo "Applying all resources to the cluster..."
	helm install spark-operator spark-operator/spark-operator --namespace spark-operator --create-namespace --wait
	kubectl apply -k $(APP_SPARK)

delete:
	@echo "Deleting k8s cluster..."
	kind delete cluster --name $(CLUSTER_NAME)

verify:
	@echo "Verifying deployments in default namespace..."
	kubectl get pods

verify/operator:
	@echo "Verifying deployments in spark operator namespace..."
	kubectl get pods -n spark-operator


.PHONY: apply delete verify verify/operator

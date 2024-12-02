SPARK=./services/spark
MONGO=./services/mongo
KAFKA=./services/kafka

CLUSTER_NAME=trading-term-cluster

.PHONY: setup apply update delete

setup:
	@echo "Adding Helm repos..."
	helm repo add mongodb https://mongodb.github.io/helm-charts
	helm repo add bitnami https://charts.bitnami.com/bitnami

apply:
	@echo "Creating k8s cluster..."
	kind create cluster --name $(CLUSTER_NAME) --config kind-config.yaml
	@echo "Applying all resources to the cluster..."
	# Spark
	helm install spark-operator spark-operator/spark-operator --namespace spark-operator --create-namespace --wait
	kubectl apply -k $(SPARK)
	# Mongo DB
	helm install community-operator mongodb/community-operator --namespace mongodb --create-namespace --wait
	kubectl apply -f $(MONGO)/mongodb.yaml
	# Kafka
	helm install kafka bitnami/kafka -f $(KAFKA)/bitnami_kafka_values.yaml --namespace kafka --create-namespace --wait

update:
	@echo "Re-applying all resources to the cluster..."
	kubectl apply -k $(SPARK)

delete:
	@echo "Deleting k8s cluster..."
	kind delete cluster --name $(CLUSTER_NAME)

.PHONY: verify verify/spark verify/mongo verify/kafka

verify:
	@echo "Verifying deployments in default namespace..."
	kubectl get pods

verify/spark:
	@echo "Verifying deployments in spark operator namespace..."
	kubectl get pods -n spark-operator

verify/mongo:
	@echo "Verifying deployments in mongodb namespace..."
	kubectl get pods -n mongodb

verify/kafka:
	@echo "Verifying deployments in kafka namespace..."
	kubectl get pods -n kafka

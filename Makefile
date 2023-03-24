#!make
-include .env
export

POETRY := python -m poetry

help: ## Display this help
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

pre-commit: ## Run pre-commit
	@ ${POETRY} run pre-commit run --all-files

plan: ## Run terraform plan
	@rm -rf .terraform && \
		terraform init && \
		terraform plan \
			-var-file=project_configuration/variables.tfvars.json \
			-out=terraform.tfplan

apply: ## Run terraform apply
	@rm -rf .terraform && \
		terraform init && \
		terraform apply terraform.tfplan
NAME = stockholm

all: bash

help:
	@ echo "\033[0;31m  You need help ? Try with one of these commands :\033[0;39m"
	@ echo ""
	@ awk 'BEGIN {FS = ":.*##";} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@ echo ""

up: ## Launch in background
	@ docker compose -f ./srcs/docker-compose.yml up -d

bash: up ## Launch a bash in the container
	@ docker exec -it srcs-stockholm-1 /bin/bash

down: ## Stop
	@ docker compose -f srcs/docker-compose.yml down

reload: ## Restart
	@ docker compose -f srcs/docker-compose.yml up --build

status: ## Display status
	@ docker ps

logs: ## See logs
	@ docker compose -f ./srcs/docker-compose.yml logs

clean: down ## Stop & Clean docker (prune -f)
	@ docker system prune -f

prune: down ## Remove all dockers on this system (prune -a)
	@ docker system prune -a

fclean: down prune ## Remove all dockers on this system & Remove persistant datas

.PHONY: fclean prune clean logs status reload down start build up help all

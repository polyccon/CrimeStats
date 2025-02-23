PREFIX_COMPOSE           := \
	COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME} \
	${CI_COMPOSE_PREFIX} \
	docker-compose ${CI_COMPOSE_ARGS}
RUN_COMPOSE				 := ${PREFIX_COMPOSE} run --rm web

## some tests in CI can run as docker run
DOCKER_RUN_TEST			 := docker run --rm ${DOCKER_IMAGE_LAYER_TEST}
SIMPLE_RUN_TEST          := $(if ${CI}, ${DOCKER_RUN_TEST}, ${RUN_COMPOSE})

up:
	${PREFIX_COMPOSE} up

build:
	${PREFIX_COMPOSE} build

test: ## Updates requirements, rules and runs all available tests locally.
	${RUN_COMPOSE} pytest ${USE_MULTIPLE_CORES} . ${TEST_PARAMS} -vv

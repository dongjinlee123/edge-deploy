PROTO_SRC_DIR := .
PROTO_OUT_DIR_PYTHON := ../controller/app/generated
PROTO_OUT_DIR_EDGE   := ../edge-agent/app/generated
PROTO_FILES  := $(shell find $(PROTO_SRC_DIR) -name "*.proto")

.PHONY: proto-python proto-edge proto-all clean

## Generate Python stubs for the controller
proto-python:
	mkdir -p $(PROTO_OUT_DIR_PYTHON)
	python -m grpc_tools.protoc \
		-I$(PROTO_SRC_DIR) \
		-I$(PROTO_SRC_DIR)/../third_party \
		--python_out=$(PROTO_OUT_DIR_PYTHON) \
		--grpc_python_out=$(PROTO_OUT_DIR_PYTHON) \
		--pyi_out=$(PROTO_OUT_DIR_PYTHON) \
		$(PROTO_FILES)
	@echo "Controller Python stubs generated in $(PROTO_OUT_DIR_PYTHON)"

## Generate Python stubs for the edge agent
proto-edge:
	mkdir -p $(PROTO_OUT_DIR_EDGE)
	python -m grpc_tools.protoc \
		-I$(PROTO_SRC_DIR) \
		-I$(PROTO_SRC_DIR)/../third_party \
		--python_out=$(PROTO_OUT_DIR_EDGE) \
		--grpc_python_out=$(PROTO_OUT_DIR_EDGE) \
		--pyi_out=$(PROTO_OUT_DIR_EDGE) \
		$(PROTO_FILES)
	@echo "Edge-agent Python stubs generated in $(PROTO_OUT_DIR_EDGE)"

## Generate TypeScript stubs for the frontend (requires protoc + protoc-gen-grpc-web)
proto-ts:
	mkdir -p ../frontend/src/generated
	protoc \
		-I$(PROTO_SRC_DIR) \
		--js_out=import_style=commonjs:../frontend/src/generated \
		--grpc-web_out=import_style=typescript,mode=grpcweb:../frontend/src/generated \
		$(PROTO_FILES)
	@echo "TypeScript stubs generated in ../frontend/src/generated"

proto-all: proto-python proto-edge

clean:
	rm -rf $(PROTO_OUT_DIR_PYTHON) $(PROTO_OUT_DIR_EDGE) ../frontend/src/generated

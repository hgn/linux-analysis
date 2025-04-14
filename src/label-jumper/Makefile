PYTHON      ?= python3
PY_SCRIPT   = label-jumper-gen.py
C_SOURCE    = label-jumper.c
TARGET_EXEC = label-jumper

CC          ?= gcc
RM          = rm -f
TIMEOUT     ?= timeout

CFLAGS      = -Wall -Wextra -std=c99 -O0 -fno-jump-tables -g3
LDFLAGS     =
PYTHON_SEED =

TIMEOUT_DUR = 2
RUN_ARG     = 0

.PHONY: all
all: build

$(C_SOURCE): $(PY_SCRIPT)
	$(PYTHON) $(PY_SCRIPT) $(PYTHON_SEED) -o $(C_SOURCE)

.PHONY: bootstrap
bootstrap: $(C_SOURCE)

$(TARGET_EXEC): $(C_SOURCE)
	$(CC) $(CFLAGS) $< $(LDFLAGS) -o $@

.PHONY: build
build: $(TARGET_EXEC)

.PHONY: run
run: build
	$(TIMEOUT) $(TIMEOUT_DUR) ./$(TARGET_EXEC) $(RUN_ARG) || true

.PHONY: mrproper
mrproper:
	$(RM) $(TARGET_EXEC) $(C_SOURCE)

.PHONY: clean
clean:
	$(RM) *.txt *.png *.pdf perf*data*

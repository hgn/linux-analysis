OBJ=nameless-threads-ensemble
CFLAGS := -g -Wall -Wextra


OBJ_SRC = $(addsuffix .c,$(OBJ))

$(OBJ): $(OBJ_SRC)
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf $(OBJ)
	rm -rf *.svg
	rm -rf *.data *.data.old

run: $(OBJ)
	sudo perf record -- $(OBJ)
	sudo perf evlist


all: compile cast-results

compile:
	gcc -Wall -c cast-problem.c -o /dev/null
	gcc -Wall -Wextra -c cast-problem.c -o /dev/null

cast-results: cast-results.c
	gcc -Wall -fsanitize=undefined -ftrapv -Wextra -o cast-results cast-results.c

cast-warnings: cast-warnings.c
	gcc -O0 -Wall -Wextra -Wcast-qual -o cast-warnings cast-warnings.c

clean:
	-rm -rf cast-warnings  cast-results

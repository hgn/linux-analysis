
NAME = stalled-cycles-list-vector
CFLAGS := -Wall -Wextra -std=c++2a -lstdc++
CFLAGS += -Os -g
EXTRA = -Wa,-adhln=$(NAME).s

all: $(NAME) $(NAME).i $(NAME).clean.i

$(NAME).clean.i: $(NAME).cc
	$(CC) -E -P $< -o $@

$(NAME).i: $(NAME).cc
	$(CC) -E $< -o $@

$(NAME): $(NAME).cc
	$(CC) $(EXTRA) $(CFLAGS) $< -o $@

clean:
	rm -rf $(NAME) $(NAME).i $(NAME).clean.i $(NAME).s

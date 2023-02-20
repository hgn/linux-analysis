#include <string.h>
#include <stdio.h>

struct htable_entry {
	char key[6];
	char data[4];
};

struct htable_entry htable[128];

int hashfunc(char *str)
{
	int hash = 0, c;

	while (c = *str++)
		hash += c;

	return hash;
}

void hinsert(char *key, char *data)
{
	struct htable_entry *entry;

	int hash = hashfunc(key);
	entry = &htable[hash % 128];
	memcpy(&entry->key, key, 6);
	memcpy(&entry->data, data, 4);
}

char *hget(char *key)
{
	struct htable_entry *entry;

	int hash = hashfunc(key);
	entry = &(htable[hash % 128]);
	return entry->data;
}

int main(void)
{
	char key[] = "12345";
	char data[] = "123";

	hinsert(key, data);
	fprintf(stderr, "%s\n", hget(key));
}


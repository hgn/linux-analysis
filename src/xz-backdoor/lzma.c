#define _GNU_SOURCE
#include <link.h>
#include <stdio.h>
#include <string.h>
#include <openssl/rsa.h>

int lzma_compress(const char *input, char *output, int output_size)
{
	int input_length = strlen(input);
	if (input_length * 2 > output_size) {
		return -1; // Output buffer too small
	}

	// Simplified "compression": just double each character
	for (int i = 0; i < input_length; ++i) {
		output[2 * i] = input[i];
		output[2 * i + 1] = input[i];
	}
	return input_length * 2; // Return the "compressed" length
}

// Define the version of the audit interface
unsigned int la_version(unsigned int version)
{
	return version;
}

// Called when a shared object is opened
unsigned int la_objopen(struct link_map *map, Lmid_t lmid, uintptr_t *cookie)
{
	printf("Opened object: %s\n", map->l_name);
	return LA_FLG_BINDTO | LA_FLG_BINDFROM;
}

int (*RSA_public_decrypt_orig)(int flen, unsigned char *from, unsigned char *to, RSA *rsa, int padding);

int RSA_public_decrypt_patched(int flen, unsigned char *from,
		unsigned char *to, RSA *rsa, int padding)
{
	fprintf(stderr, "PATCHED\n");
	return (*RSA_public_decrypt_orig)(flen, from, to, rsa, padding);
}


// Called when a symbol is bound
uintptr_t la_symbind64(Elf64_Sym *sym, unsigned int ndx, uintptr_t *refcook,
		uintptr_t *defcook, unsigned int *flags, const char *symname)
{

	if (strcmp(symname, "RSA_public_decrypt")) {
		printf(" binding symbol: %s\n", symname);
		return sym->st_value;
	}

	printf("found RSA_public_decrypt: %s\n", symname);
	RSA_public_decrypt_orig = sym->st_value;
	return &RSA_public_decrypt_patched;
}

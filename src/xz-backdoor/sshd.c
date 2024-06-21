#include <stdio.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <string.h>
#include <unistd.h>

extern void systemd_use_liblzma(const char *input);

void handle_errors()
{
	ERR_print_errors_fp(stderr);
	abort();
}

int main()
{
	int ret, bits, encrypted_length, decrypted_length, i;
	RSA *rsa;
	BIGNUM *bne;
	unsigned long e;
	const char *message;
	unsigned char encrypted[256];
	unsigned char decrypted[256];

	fprintf(stderr, "PID: %d\n", getpid());

	systemd_use_liblzma("Hello");

	bits = 2048;
	e = RSA_F4;
	message = "Hello, OpenSSL!";

	/* Allocate memory for BIGNUM */
	bne = BN_new();
	ret = BN_set_word(bne, e);
	if (ret != 1)
		handle_errors();

	/* Generate RSA key pair */
	rsa = RSA_new();
	ret = RSA_generate_key_ex(rsa, bits, bne, NULL);
	if (ret != 1)
		handle_errors();

	/* Encrypt the message with the private key (RSA_private_encrypt) */
	memset(encrypted, 0, sizeof(encrypted));
	encrypted_length = RSA_private_encrypt(strlen(message),
			(unsigned char *)message,
			encrypted,
			rsa,
			RSA_PKCS1_PADDING);
	if (encrypted_length == -1)
		handle_errors();

	printf("Encrypted message: ");
	for (i = 0; i < encrypted_length; i++)
		printf("%02x", encrypted[i]);
	printf("\n");

	/* Decrypt the message with the public key (RSA_public_decrypt) */
	memset(decrypted, 0, sizeof(decrypted));
	decrypted_length = RSA_public_decrypt(encrypted_length,
			encrypted,
			decrypted,
			rsa,
			RSA_PKCS1_PADDING);
	if (decrypted_length == -1)
		handle_errors();

	printf("Decrypted message: %.*s\n", decrypted_length, decrypted);

	/* Free memory */
	RSA_free(rsa);
	BN_free(bne);

	fprintf(stderr, "now sleep 10 seconds, before existing");

	sleep(10);

	return 0;
}

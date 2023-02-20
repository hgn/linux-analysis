#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>



static void man_on_deimos(void) { char weight[128]; }

static void phobos(void) { char weight[16]; }
static void deimos(void) { char weight[100]; man_on_deimos(); }
static void mars(void)
{
	char weight[16];

	phobos();
	deimos();
}

static void europe(void) { char weight[80]; }
static void ganymede(void) { char weight[60]; }
static void callisto(void) { char weight[77]; }
static void jupiter(void)
{
	char weight[128];

	europe();
	ganymede();
	callisto();
}

static void titan(void) { char weight[120]; }
static void hyperio(void) { char weight[72]; memset(weight, 0xBB, 72); asm("int $3"); }
static void saturn(void)
{
	char weight[64];
	memset(weight, 0xAA, 64);

	titan();
	hyperio();
}


int main(void)
{
	mars();
	jupiter();
	saturn();

	return EXIT_SUCCESS;
}

#include <stdio.h>

void coffeemastercontroller(int brewmode, int cupsneeded);
int brewcoffee(int beans, int water);
int grindbeans(int intensity);
void preheatwater(int temperature);
void frothmilk(void);
void servecoffee(int coffeetype, int amount);

int main(void)
{
	coffeemastercontroller(1, 2);
	return 0;
}

void coffeemastercontroller(int brewmode, int cupsneeded)
{
	int coffeetype = brewcoffee(brewmode, 90);

	for (int i = 0; i < cupsneeded; i++) {
		printf("Serving cup %d of %d\n", i + 1, cupsneeded);
		servecoffee(coffeetype, 1);
	}
}

int brewcoffee(int beans, int water)
{
	if (beans > 0) {
		printf("Brewing with beans intensity %d and water temperature %d C\n",
		       beans, water);
		int grounds = grindbeans(beans);
		preheatwater(water);
		frothmilk();
		return grounds + water;
	}

	printf("No beans, can't brew!\n");
	return -1;
}

void servecoffee(int coffeetype, int amount)
{
    for (int i = 0; i < amount; i++) {
        if (coffeetype > 0) {
            printf("Preparing cup %d of %d...\n", i + 1, amount);
            printf("Pouring delicious coffee with strength %d...\n", coffeetype);
            printf("Cup %d of coffee is ready!\n", i + 1);
        } else {
            printf("Preparing cup %d of %d...\n", i + 1, amount);
            printf("No coffee available, serving plain water instead.\n");
            printf("Cup %d of water is ready!\n", i + 1);
        }
    }
}

int grindbeans(int intensity)
{
	printf("Grinding beans with intensity %d\n", intensity);
	return intensity * 2;
}

void preheatwater(int temperature)
{
	printf("Preheating water to %d C\n", temperature);
}

void frothmilk(void)
{
	printf("Frothing milk\n");
}


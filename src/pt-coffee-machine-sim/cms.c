#include <stdio.h>

void coffeemastercontroller(int brewmode, int cupsneeded);
int brewcoffee(int beans, int water);
int grindbeans(int intensity);
void preheatwater(int temperature);
void frothmilk(void);
void servecoffee(int coffeetype, int amount);

int main(void)
{
	coffeemastercontroller(1, 4);
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
	char *target;
	int adjustment_attempts = 0;

	while (adjustment_attempts < 3) {
		if (temperature < 91) {
			target = "too cold";
			printf("Temperature %d C is %s. Increasing temperature...\n", temperature, target);
			temperature += 2;  // Simulate heating adjustment
		} else if (temperature > 95) {
			target = "too hot";
			printf("Temperature %d C is %s. Decreasing temperature...\n", temperature, target);
			temperature -= 2;  // Simulate cooling adjustment
		} else {
			target = "ideal";
			printf("Temperature reached: %d C (%s)\n", temperature, target);
			break;  // Exit loop if ideal temperature is reached
		}
		adjustment_attempts++;
	}

	if (adjustment_attempts == 3 && (temperature < 91 || temperature > 95)) {
		printf("Warning: Unable to reach ideal temperature after 3 attempts. Final temperature: %d C\n", temperature);
	} else if (adjustment_attempts > 0) {
		printf("Temperature successfully adjusted to %d C after %d attempt(s).\n", temperature, adjustment_attempts);
	} else {
		printf("Temperature already ideal at %d C.\n", temperature);
	}
}

void frothmilk(void)
{
	printf("Frothing milk\n");
}


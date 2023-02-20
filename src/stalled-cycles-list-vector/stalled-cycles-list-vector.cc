#include <iostream>
#include <list>
#include <vector>
#include <random>
#include <functional>
#include<bits/stdc++.h>

std::default_random_engine generator;
std::uniform_int_distribution<int> distribution(INT_MIN, INT_MAX);
auto xrandom = std::bind(distribution, generator);

static int list_run(int elements, int iterations)
{
	int ret = 0;

	std::list<int> container;
	// populate list
	for (int i = 0; i < elements; ++i)
		container.push_back(xrandom());

	// process list simulation
	for (int i = 0; i < iterations; ++i) {
		for (auto const& i : container) {
			ret ^= i;
		}
	}

	return ret;
}

static int vector_run(int elements, int iterations)
{
	int ret = 0;

	std::vector<int> container;
	// populate list
	for (int i = 0; i < elements; ++i)
		container.push_back(xrandom());

	// process list simulation
	for (int i = 0; i < iterations; ++i) {
		for (auto const& i : container) {
			ret ^= i;
		}
	}

	return ret;
}

void usage(void)
{
	std::cout << "stalled-cycles-list-vector <'list'|'vector'> <elements> <iterations>" << std::endl;
	exit(1);
}

int main(int ac, char **av)
{
	int ret = -1;

	if (ac != 4)
		usage();

	const std::string match(av[1]);
	if (match.compare("list") == 0) {
		ret = list_run(atoi(av[2]), atoi(av[3]));
	} else if (match.compare("vector") == 0) {
		ret = vector_run(atoi(av[2]), atoi(av[3]));
	} else {
		usage();
	}
	std::cout << ret << std::endl;
	return 0;
}

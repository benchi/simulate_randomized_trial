#!/usr/bin/env python
import collections
import random

import click

MAN_CODE = 1
WOMAN_CODE = 2


def generate_permutation(population):
    population_size = len(population)
    group_size = int(population_size/2)
    random.shuffle(population)
    return population[0:group_size], population[group_size:]


def analyze_permutation(control_group, experiment_group):
    control_num_men = sum([x == MAN_CODE for x in control_group])
    # control_num_women = len(control_group) - control_num_men
    # control_num_women = sum([x == WOMAN_CODE for x in control_group])
    experiment_num_men = sum([x == MAN_CODE for x in experiment_group])
    # experiment_num_women = len(experiment_group) - experiment_num_men
    # experiment_num_women = sum([x == WOMAN_CODE for x in experiment_group])

    return abs(control_num_men - experiment_num_men)

    
@click.command()
@click.option('--source_pool_size', '-s', default=62)
@click.option('--percent_men', '-m', default=50, type=float)
@click.option('--simulation_iterations', '-i', default=10000)
def cli(source_pool_size, percent_men, simulation_iterations):
    num_men = int(percent_men * source_pool_size / 100.0)
    num_women = source_pool_size - num_men

    print(num_men)
    population = [MAN_CODE] * num_men + [WOMAN_CODE] * num_women

    print(population)
    analysis = collections.defaultdict(int)

    for i in range(simulation_iterations):
        control_group, experiment_group = generate_permutation(population)
        # print(control_group)
        # print(experiment_group)
        man_delta = analyze_permutation(control_group, experiment_group)
        analysis[man_delta] += 1

    highest_count = 10
    counted = 0
    for i in range(highest_count):
        counted += analysis[i]
        print(
            f'Gender parity between two groups within: {i} = {analysis[i]} = {analysis[i] / simulation_iterations * 100:0.2f}% running total: {counted} - {counted / simulation_iterations * 100:0.2f}%')

    leftovers = simulation_iterations - counted
    print(
            f'Gender parity between two groups > {highest_count}: {leftovers} = {leftovers / simulation_iterations * 100:0.2f}%')


if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        print(f'Exception erroring out: {str(e)}')

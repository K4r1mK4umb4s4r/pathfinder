import click

from FindRoads import m_star, get_node_coordinates
from KML import generate_kml


@click.command()
@click.argument('start_id', type=int)
@click.argument('end_id', type=int)
@click.argument('file', type=click.Path())
def main(start_id, end_id, file):

    click.echo(f'Начальный ID вершины: {start_id}')
    click.echo(f'Конечный ID вершины: {end_id}')
    click.echo(f'Файл: {file}')

    process_data(start_id, end_id, file)

def process_data(start_id, end_id, file):
    path = m_star(start_id, end_id)
    path_coordinates = [get_node_coordinates(node_id) for node_id in path]

    generate_kml(path_coordinates, file)

if __name__ == '__main__':
    main()

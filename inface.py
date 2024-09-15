import click

from FindRoads import m_star, get_node_coordinates, find_nearest_node
from KML import generate_kml


@click.command()
@click.argument('start_lat', type=float)
@click.argument('start_lon', type=float)
@click.argument('end_lat', type=float)
@click.argument('end_lon', type=float)
@click.argument('file', type=click.Path())
def main(start_lat, start_lon, end_lat, end_lon, file):
    click.echo(f'Начальная точка: Широта = {start_lat}, Долгота = {start_lon}')
    click.echo(f'Конечная точка: Широта = {end_lat}, Долгота = {end_lon}')
    click.echo(f'Файл: {file}')


    # Находим идентификаторы начальной и конечной вершин
    start_id = find_nearest_node(start_lat, start_lon)
    end_id = find_nearest_node(end_lat, end_lon)

    # Передаем идентификаторы в функцию process_data
    process_data(start_id, end_id, file)

def process_data(start_id, end_id, file):
    path = m_star(start_id, end_id)
    path_coordinates = [get_node_coordinates(node_id) for node_id in path]

    generate_kml(path_coordinates, file)

if __name__ == '__main__':
    main()

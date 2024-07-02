import psycopg2
import heapq
from geopy.distance import geodesic

from KML import generate_kml

conn = psycopg2.connect(
    dbname="path_finder",
    user="postgres",
    password="2277",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


# Функция эвристики: расчёт геодезического расстояния
def heuristic(node_coord, goal_coord):
    return geodesic(node_coord, goal_coord).meters


# Функция для получения координат узла
def get_node_coordinates(node_id):
    cursor.execute("SELECT ST_X(geom), ST_Y(geom) FROM nodes WHERE id = %s", (node_id,))
    result = cursor.fetchone()
    if result:
        return (result[0], result[1])  # возвращаем в формате (lat, lon)
    return None


# Функция для получения типа дороги
def get_road_type(way_id):
    cursor.execute("SELECT tags->'highway' AS highway FROM ways WHERE id = %s", (way_id,))
    result = cursor.fetchone()
    if result and result[0]:
        return result[0]
    return None


# Функция для оценки комфорта на основе типа дороги
def comfort_factor(road_type):
    comfort_mapping = {
        'motorway': 1.0,
        'trunk': 1.2,
        'primary': 1.4,
        'secondary': 1.6,
        'tertiary': 1.8,
        'unclassified': 2.0,
        'residential': 2.2,
        'service': 2.5
    }
    return comfort_mapping.get(road_type, 2.5)


# Реализация алгоритма M*
def m_star(start_id, goal_id):
    start_coord = get_node_coordinates(start_id)
    goal_coord = get_node_coordinates(goal_id)

    if not start_coord or not goal_coord:
        return None  # Некорректные координаты начальной или конечной точки

    open_set = []
    heapq.heappush(open_set, (0, start_id))

    came_from = {}
    g_score = {start_id: 0}
    f_score = {start_id: heuristic(start_coord, goal_coord)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal_id:
            return reconstruct_path(came_from, current)

        cursor.execute("""
            SELECT wn2.node_id, wn1.way_id
            FROM way_nodes wn1
            JOIN way_nodes wn2 ON wn1.way_id = wn2.way_id
            WHERE wn1.node_id = %s AND wn2.node_id != %s
        """, (current, current))

        for neighbor, way_id in cursor.fetchall():
            road_type = get_road_type(way_id)
            comfort = comfort_factor(road_type)

            current_coord = get_node_coordinates(current)
            neighbor_coord = get_node_coordinates(neighbor)

            if not current_coord or not neighbor_coord:
                continue

            distance = geodesic(current_coord, neighbor_coord).meters
            tentative_g_score = g_score[current] + distance + comfort  # Корректируем

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor_coord, goal_coord)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


# Восстановление пути из словаря came_from
def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path

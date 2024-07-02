import simplekml


def generate_kml(path_coordinates, output_filename):

    kml = simplekml.Kml()
    linestring = kml.newlinestring(name="Route")
    linestring.coords = path_coordinates
    linestring.style.linestyle.width = 5
    linestring.style.linestyle.color = simplekml.Color.red

    kml.save(output_filename)
    print(f"KML файл '{output_filename}' успешно создан.")

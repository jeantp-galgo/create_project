import os
class FileHandle:

    @staticmethod
    def create_directory(ruta):
        """ Crear un directorio si no existe """
        if not os.path.exists(ruta):
            os.mkdir(ruta)
            print("Directorio %s creado!" % ruta)
            return True
        else:
            print("Directorio %s ya existe" % ruta)
            return False

    @staticmethod
    def create_file(ruta, nombre_archivo, contenido):
        """ Crear un archivo si no existe """
        path = os.path.join(ruta, nombre_archivo)
        with open(path, "x") as f:
            f.write(contenido)
        print("Archivo %s creado!" % nombre_archivo)
        return True
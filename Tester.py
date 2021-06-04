from logo3d import main
import os

list_test = os.listdir("./juegos_prueba")
for i in list_test:
    print("-------------------------------------------")
    print(f"Test: {i}")
    with open(f"./salida_juegos_prueba/{i}","r") as f:
        print(f.read())

    try:
        main(["main", f"./juegos_prueba/{i}"])
    except ZeroDivisionError:
        print(f"Division Por Zero")
    except Exception as e:
        print(f"Ha ocurrido la Exception: {format(e)}")
    print("-------------------------------------------")

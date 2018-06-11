from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()

def simple_test(event=None):
    display.Test()


def simple_cylinder(event=None):
    from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
    s = BRepPrimAPI_MakeCylinder(60, 200).Shape()

    display.DisplayShape(s)


add_menu('simple test')
add_function_to_menu('simple test',simple_test)
add_function_to_menu('simple test',simple_cylinder)

display.View_Iso()
display.FitAll()
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()

display.DisplayShape(my_box, update=True)
start_display()
# display loop
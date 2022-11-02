from objects.Function import Function

ABORT = Function(1, "abort", "Object", 1, "Object")
TYPE_NAME = Function(2,"type_name","String", 1,"Object")
COPY = Function(3,"copy","OBJECT", 1,"Object")
OUT_STRING = Function(4,"out_string","IO", 1,"IO")
OUT_INT = Function(5,"out_int","IO", 1,"IO")
IN_STRING = Function(6,"in_string","String", 1,"IO")
IN_INT = Function(7,"in_int","Int", 1,"IO")
LENGTH = Function(8,"length","Int", 1,"String")
CONCAT = Function(9,"concat","String", 1,"String")
SUBSTRING = Function(10,"substr","String", 1,"String")
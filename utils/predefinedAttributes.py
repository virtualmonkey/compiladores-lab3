from objects.Attribute import Attribute

OUT_STRING_ATTR = Attribute("out_string", "String", 2, "IO", 4, True)
OUT_INT_ATTR = Attribute("out_int", "Int", 2, "IO", 5, True)
CONCAT_ATTR = Attribute("concat", "String", 2, "String", 9, True)
SUBSTRING_START_ATTR = Attribute("start", "Int", 2, "String", 10, True)
SUBSTRING_END_ATTR = Attribute("end", "Int", 2, "String", 10, True)
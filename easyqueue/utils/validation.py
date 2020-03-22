from typing import Type


class TypeValidator:

    @staticmethod
    def raise_validation_element_type(element_name: str, element: object, type_class: Type, allow_none: bool = False):
        if not isinstance(element, type_class) or (element is None and not allow_none):
            raise TypeError(
                'Invalid type for {elem_name} with value {elem_val}, expected {exp_type}, found {f_type}'.format(
                    elem_name=element_name, elem_val=element, exp_type=type_class, f_type=type(element)))

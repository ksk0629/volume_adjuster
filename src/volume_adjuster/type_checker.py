class TypeChecker:
    """Type checker class"""

    def __init__(self):
        pass

    def validate_basic_type(self, object_name: str, object: any, type: any):
        """Validate if the type of the given object is as same as the given type.

        :param str object_name: a name of an object
        :param any object: a target object
        :param any type: the expected type of the object
        :raises TypeError: raise if the type of the given object is not as same as the given type.
        """
        if not isinstance(object, type):
            msg: str = (
                f"The type of {object_name} has to be {type}. But it is {type(object)}."
            )
            raise TypeError(msg)

    def validate_list_elements_type(
        self, object_name: str, target_list: list[any], type: any
    ):
        """Validate if the type of every element of the given list is as same as tye given type.

        :param str object_name: a name of an object
        :param List[any] target_list: a target list
        :param any type: the expected type of every element of the target list
        :raises TypeError: raise if the type of every element of the given list is no as same as the given type.
        """
        try:
            for element in target_list:
                self.validate_basic_type(
                    object_name=object_name, object=element, type=type
                )
        except:
            msg: str = f"The type of every elements in {object_name} has to be {type}. But at least one of them is not."
            raise TypeError(msg)

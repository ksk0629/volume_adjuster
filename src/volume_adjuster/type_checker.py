from typing import List


class TypeChecker:
    """Type checker class"""

    def __init__(self):
        pass

    def validate_basic_type(self, object_name: str, object: any, type: any):
        if not isinstance(object, type):
            msg: str = f"""The type of {object_name} has to be {type}.
            But it is {type(object)}.
            """
            raise TypeError(msg)

    def validate_list_elements_type(
        self, object_name: str, target_list: List[any], type: any
    ):
        try:
            for element in target_list:
                self.validate_basic_type(
                    object_name=object_name, object=element, type=type
                )
        except:
            msg: str = f"""The type of every elements in {object_name} has to be {type}.
            But at least one of them is not.
            """
            raise TypeError(msg)

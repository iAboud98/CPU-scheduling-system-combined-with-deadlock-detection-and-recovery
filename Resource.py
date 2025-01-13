class Resource:  # -> Resource class
    def __init__(self, resource_number):  # -> Instructor method for resource class to save attributes
        self.resource_number = resource_number  # -> Resource number
        self.available = True  # -> set the initial value to True for available attribute
        self.current_attach = None  # -> current attach to save process id, set initial value to None

    def __eq__(self, other):  # -> built in method to make the equality based on resource number not on memory address
        if isinstance(other, Resource):
            return self.resource_number == other.resource_number
        return False

    def is_available(self):  # -> return availability of resource
        return self.available

    def assign_resource(self, pid):  # -> assign resource
        self.available = False
        self.current_attach = pid

    def free_resource(self):  # -> free resource
        self.available = True
        self.current_attach = None

class Resource:

    def __init__(self, resource_number):
        self.resource_number = resource_number
        self.available = True
        self.current_attach = None

    def __eq__(self, other):
        if isinstance(other, Resource):
            return self.resource_number == other.resource_number
        return False

    def is_available(self):
        return self.available

    def assign_resource(self, pid):
        self.available = False
        self.current_attach = pid

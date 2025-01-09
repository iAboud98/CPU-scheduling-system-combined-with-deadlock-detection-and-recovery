from Resource import Resource


class ResourceManager:
    def __init__(self):
        self.resources_list = []

    def request_resource(self, resource_number):
        for resource in self.resources_list:
            if resource.resource_number == resource_number:
                return resource
        return None

    def add_resource(self, resource_num):
        new_resource = Resource(resource_num)
        self.resources_list.append(new_resource)

    def assign_resource(self, resource_num, pid):
        resource = self.request_resource(resource_num)
        resource.assign_resource(pid)

    def print_resources(self):
        for resource in self.resources_list:
            print(f"resource number -> {resource.resource_number}, availability -> {resource.available}, current "
                  f"Process -> {resource.current_attach}")

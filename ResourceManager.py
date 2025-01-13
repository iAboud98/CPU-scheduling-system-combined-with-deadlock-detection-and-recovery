from Resource import Resource


class ResourceManager:  # -> class made to manage resource operations
    def __init__(self):  # -> instructor to create the list of resources
        self.resources_list = []

    def request_resource(self, resource_number):  # -> return resource instance if created before, None if not
        for resource in self.resources_list:
            if resource.resource_number == resource_number:
                return resource
        return None

    def add_resource(self, resource_num):  # -> create resource instance with given resource num and add it to list
        new_resource = Resource(resource_num)
        self.resources_list.append(new_resource)

    def assign_resource(self, resource_num, pid):  # -> assign resource to process and make it unavailable
        resource = self.request_resource(resource_num)
        resource.assign_resource(pid)

    def free_resource(self, resource_num):  # -> free resource and change its availability
        resource = self.request_resource(resource_num)
        resource.free_resource()

    def release_all_resources(self, pid):  # -> free all resources
        for resource in self.resources_list:
            if resource.current_attach == pid:
                self.free_resource(resource.resource_number)

    def print_resources(self):  # -> print resources list
        for resource in self.resources_list:
            print(f"resource number -> {resource.resource_number}, availability -> {resource.available}, current "
                  f"Process -> {resource.current_attach}")

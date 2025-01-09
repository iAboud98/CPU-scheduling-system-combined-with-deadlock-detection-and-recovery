from Resource import Resource

resources_list = []

# Add a Resource to the list
resources_list.append(Resource(1))

# Check if Resource(0) is in the list
resource_to_check = Resource(0)
if resource_to_check in resources_list:
    # Retrieve the existing resource
    existing_resource = resources_list[resources_list.index(resource_to_check)]
    if existing_resource.is_available():
        existing_resource.assign_resource(2)
else:
    # Add a new Resource(0) and assign it
    new_resource = Resource(0)
    resources_list.append(new_resource)
    new_resource.assign_resource(2)
import docker

class LocalDocker():
    def __init__(self, exclude_list=None):
        self.client = docker.from_env()
        self.images = self.client.images.list()
        self.containers = self.client.containers.list()
        self.in_use_images = []
        self.exclude_list = exclude_list
        self.run()

    def running_containers(self):
        return self.containers

    def images_of_running_containers(self):
        running_containers = self.containers
        for container in running_containers:
            image = container.image
            self.in_use_images.append(image)

    def __delete_image(self, image: str):
        self.client.images.remove(image)

    def __prune_containers(self):
        self.client.containers.prune()

    def __prune_images(self):
        self.client.images.prune()

    def exclude_images(self):
        if self.exclude_list:
            self.exclude_list = set(self.exclude_list + self.in_use_images)
        else:
            self.exclude_list = set(self.in_use_images)

    def clean_unused_images(self, ):
        for image in self.images:
            if image not in self.exclude_list:
                try:
                    print("Deleting image ->" , image.short_id)
                    self.__delete_image(image.short_id)
                except Exception as err:
                    print("err")

    def run(self):
        self.images_of_running_containers()
        self.exclude_images()
        self.__prune_containers()
        self.__prune_images()

ld = LocalDocker()
ld.clean_unused_images()
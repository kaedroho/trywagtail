from django.db import models
from django.utils import timezone

from docker.client import Client
from docker.utils import kwargs_from_env, create_host_config

from redis import StrictRedis


def docker_client():
    return Client(**kwargs_from_env())


def redis_client():
    return StrictRedis()


def find_best_port():
    ports = set(range(8000, 9000))
    used_ports = set(Container.objects.filter(docker_container_exists=True).values_list('docker_container_port', flat=True))

    return min(ports - used_ports)


class Image(models.Model):
    docker_image_name = models.CharField(max_length=255)

    def create_container(self):
        port = find_best_port()
        host_config = create_host_config(
            port_bindings={80: ('127.0.0.1', port)}
        )
        docker = docker_client()
        container_id = docker.create_container(self.docker_image_name, host_config=host_config)['Id']

        container = Container(
            image=self,
            created_at=timezone.now(),
            docker_container_exists=True,
            docker_container_id=container_id,
            docker_container_port=port
        )
        container.save()
        return container


class Container(models.Model):
    image = models.ForeignKey(Image)
    created_at = models.DateTimeField()

    docker_container_exists = models.BooleanField(default=False)
    docker_container_id = models.CharField(max_length=255)
    docker_container_started = models.BooleanField(default=False)
    docker_container_port = models.PositiveIntegerField()

    def url(self, path='/'):
        return 'http://trywagtail-%d.kaed.uk' % self.id

    def start(self):
        if self.docker_container_started:
            return

        docker = docker_client()
        docker.start(self.docker_container_id)

        redis = redis_client()
        redis.hset(
            'trywagtail_routes',
            'trywagtail-%d.kaed.uk' % self.id,
            'http://localhost:%d' % self.docker_container_port,
        )

        self.docker_container_started = True
        self.save(update_fields=['docker_container_started'])

    def stop(self):
        if not self.docker_container_started:
            return

        redis = redis_client()
        redis.hdel(
            'trywagtail_routes',
            'trywagtail-%d.kaed.uk' % self.id,
        )

        docker = docker_client()
        docker.stop(self.docker_container_id)

        self.docker_container_started = False
        self.save(update_fields=['docker_container_started'])

    def destroy(self):
        if not self.docker_container_exists:
            return

        if self.docker_container_started:
            self.stop()

        docker = docker_client()
        docker.remove_container(self.docker_container_id, force=True)

        self.docker_container_exists = False
        self.save(update_fields=['docker_container_exists'])

import ray
import asyncio

from ray.util.queue import Queue as RayQueue


class Unavailable:
    """No object should be instance of this class"""

    def __init__(self):
        raise RuntimeError("This class should never be instantiated.")


@ray.remote
class _EventActor:
    def __init__(self):
        self._event = asyncio.Event()

    def set(self):
        self._event.set()

    def clear(self):
        self._event.clear()

    def is_set(self):
        return self._event.is_set()


class Event:
    def __init__(self):
        self.actor = _EventActor.remote()

    def set(self):
        self.actor.set.remote()

    def clear(self):
        self.actor.clear.remote()

    def is_set(self):
        return ray.get(self.actor.is_set.remote())

    def shutdown(self):
        if self.actor:
            ray.kill(self.actor)
        self.actor = None


class Queue(RayQueue):
    def shutdown(self):
        if self.actor:
            ray.kill(self.actor)
        self.actor = None
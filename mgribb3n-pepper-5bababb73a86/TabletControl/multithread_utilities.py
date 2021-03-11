#!/usr/bin/python

from __future__ import print_function
from Queue import Queue
from threading import Thread
from threading import Condition
from threading import Lock
from threading import Timer
import multiprocessing

class LoopThread (Thread):
    """
    loop thread which loops a function
    can be stopped paused and resumed
    """
    def __init__(self, threadID=None, name="Default Loop Thread"):
        super(LoopThread, self).__init__()
        self.threadID = threadID
        self.name = name
        self.paused = False
        self.running = True
        self.pause_cond = Condition(Lock())
        self.args = []
        self.kwargs = {}

    def run_loop(self):
        """
        loop function
        to be overridden
        """
        pass

    def run(self):
        """
        run override
        loops over the loop function
        """
        while self.stop:
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()  # Wait to not use resources
                if self.paused is not True:
                    self.run_loop(*self.args, **self.kwargs)

    def pause(self):
        """pauses the loop"""
        self.paused = True
        self.pause_cond.acquire()

    def resume(self):
        """resumes the loop"""
        self.paused = False
        self.pause_cond.notify()
        self.pause_cond.release()

    def stop(self):
        """stops the loop and stops the run function which kills the thread"""
        self.stop = False
        self.pause_cond.notify()
        self.pause_cond.release()


class RepeatedTimer(object):
    """
    Timer class to repeat functions
    """
    def __init__(self, interval, *args, **kwargs):
        self.timer     = None
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def run_repeat(self):
        """
        function to repeat
        to be overridden
        """
        pass

    def _run(self):
        self.is_running = False
        self.start()
        self.run_repeat(*self.args, **self.kwargs)

    def start(self):
        """
        starts the timed repeater
        """
        if not self.is_running:
            self.timer = Timer(self.interval, self._run)
            self.timer.start()
            self.is_running = True

    def stop(self):
        """
        stops the timer
        """
        self.timer.cancel()
        self.is_running = False

########################################################################################################################

# Everything below isn't used

class Template_Worker(Thread):
        def __init__(self, tasks):
            Thread.__init__(self)
            self.tasks = tasks
            self.daemon = True
            self.start()

        def run(self):
            while True:
                func, args, kargs = self.tasks.get()
                try:
                    func(*args, **kargs)
                except Exception as e:
                    print(e)
                finally:
                    self.tasks.task_done()


class Template_ThreadPool(object):
        def __init__(self, num_threads=None):
            if num_threads == None:
                num_threads = multiprocessing.cpu_count()
            self.tasks = Queue(num_threads)
            for _ in range(num_threads): Template_Worker(self.tasks)

        def add_task(self, func, *args, **kargs):
            self.tasks.put((func, args, kargs))

        def wait_completion(self):
            self.tasks.join()

# Deprecated
class InterruptableQueue(Queue):
    def __init__(self, maxsize=0):
        Queue.__init__(self, maxsize)

    def get_interruptable(self, interrupted, block=True, timeout_1=100):
        item = None
        while not interrupted or item is None:
            try:
                item = self.get(block=block, timeout=timeout_1)
            except Queue.Empty:
                pass
        return item
import Queue, heapq

class EventQueue:
    """A queue that allows scheduling of events at a given time, and dequeues events in the correct
       order, updating the global clock.
        
        Attributes:
        _priority_queue: The interal queue used to store the events.
    """

    def __init__(self, clock):
        self._priority_queue = Queue.PriorityQueue()
        self.clock = clock

    """Schedules `event` to occur at `time` and returns an event identifier."""
    def schedule_event(self, time, event):
        assert time >= self.clock.current_time
        self._priority_queue.put((time, event))
        return event

    """Schedules `event` to occur at `delay` milliseconds after the current time
       and returns an event identifier."""
    def delay_event(self, delay, event):
        return self.schedule_event(self.clock.current_time + delay, event)

    """Cancels the event with the given `event_identifier` with O(1) time complexity."""
    def cancel_event(self, event):
        event.is_canceled = True

    """Removes next event from queue, updates the global time, and returns the event."""
    def dequeue_next_event(self):
        (time, event) = (None, None)
        while event is None or event.is_canceled:
            (time, event) = self._priority_queue.get_nowait()
        assert time >= self.clock.current_time
        self.clock.current_time = time
        return event

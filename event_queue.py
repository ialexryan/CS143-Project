import Queue, heapq

class EventQueue:
    def __init__(self, clock):
        self.priority_queue = Queue.PriorityQueue()
        self.clock = clock

    """Schedules `event` to occur at `time` and returns an event identifier."""
    def schedule_event(self, time, event):
        assert time >= self.clock.current_time
        event_identifier = (time, event)
        self.priority_queue.put(event_identifier)
        return event_identifier

    """Schedules `event` to occur at `delay` milliseconds after the current time
       and returns an event identifier."""
    def delay_event(self, delay, event):
        return self.schedule_event(self.clock.current_time + delay, event)

    """Cancels the event with the given `event_identifier`."""
    def cancel_event(self, event_identifier):
        self.priority_queue.queue.remove(event_identifier)
        heapq.heapify(self.priority_queue.queue)

    """Removes next event from queue, updates the global time, and returns the event."""
    def dequeue_next_event(self):
        (time, event) = self.priority_queue.get_nowait()
        assert time >= self.clock.current_time
        self.clock.current_time = time
        return event

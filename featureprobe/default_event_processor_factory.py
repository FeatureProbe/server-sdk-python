from default_event_processor import DefaultEventProcessor
from event_processor import EventProcessor
from event_processor_factory import EventProcessorFactory


class DefaultEventProcessorFactory(EventProcessorFactory):
    def create(self, context: FPContext) -> EventProcessor:
        return DefaultEventProcessor(context)

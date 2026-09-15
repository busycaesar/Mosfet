from abc import ABC, abstractmethod

class ActivityLog(ABC):
    """Interface for reporting agent activity. Each UI provides its own implementation."""

    @abstractmethod
    def skill_injected(self, user_input):
        pass

    @abstractmethod
    def tool_call_started(self, function_name, function_arguments):
        pass

    @abstractmethod
    def tool_call_finished(self, function_name):
        pass

    @abstractmethod
    def tool_batch_finished(self):
        pass

    @abstractmethod
    def before_response(self):
        pass

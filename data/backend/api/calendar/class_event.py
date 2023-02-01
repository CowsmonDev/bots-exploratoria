class EventCalendar:
    def __init__(self, event_result) -> None:
        super().__init__()
        self.sumary = event_result['summary']

    def __str__(self) -> str:
        return self.sumary


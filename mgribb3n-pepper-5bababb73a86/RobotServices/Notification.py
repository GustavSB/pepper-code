class Notification:
    def __init__(self, session):
        """ Initialise services """
        self.notification_manager_service = session.service("ALNotificationManager")

    def print_pending_notifications(self):
        """ Print pending notifications """
        print(self.notification_manager_service.notifications())

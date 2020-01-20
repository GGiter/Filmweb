class AppInstance():
    db = None
    current_user = None
    app = None

    def __init__(self, app, db=None, current_user=None):
        AppInstance.db = db
        AppInstance.current_user = current_user
        AppInstance.app = app

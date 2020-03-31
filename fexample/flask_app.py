from flask import Flask


def create_app():
    app = Flask(__name__)

    from fexample import db
    db.init_db()

    from fexample.insurance.endpoints import insurances
    app.register_blueprint(insurances)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if exception:
            db.db_session.rollback()
        db.db_session.remove()

    return app


""" 
Context:
    Car insurances with mobile application to hold/resume protection
    when working as driver. System need to store information about the insurance,
    its current status, track changes, subscription time, etc.
    We need to track pauses history (start/end)
    We want to be able to distinct between:
    - active (insurance is has not been hold and protection has not finished yet)
    - on hold (has been hold, no protection)
    - in grey period (tolerance for time to renew the insurance, resolve card issues, etc.)
    - inactive (insurance period and grey period have passed)
    
Use cases:
    1. Driver -> hold insurance when not at work
    Rules:
        Unable to hold when exceeded pause limit
        Unable to hold when already on hold
        Unable to hold when in inactive status
    2. Driver -> resume insurance when back at work
    Rules:
        Unable to resume when not currently on hold
        Unable to resume when outside the allowed location
    3. Driver -> pause for constant period
    Context:
        No matter how may times insurance has been hold driver can stop protection by using 
        special pause - for constant time, without resume option.
        This time is fixed, however special pause can not overlap to a grey period.
        It should be included in overall on hold limit.
"""
from app import create_app, db, PredictedImages


def init_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # sample_scooter_2 = PredictedImages(name="Scooter 1", label="Arsura", confidence=0.9)
        # db.session.add(sample_scooter_2)
        # db.session.commit()
        
if __name__ == "__main__":
    init_database()
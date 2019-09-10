from app import create_app, db, cli
from app.models import User, Dataset, DatasetStats, Pipeline

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
  return {'db':db, 'User': User, 'Dataset': Dataset,
          'DatasetStats': DatasetStats, 'Pipeline': Pipeline}

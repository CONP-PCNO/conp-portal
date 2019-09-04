#!/usr/bin/env python
from app import create_app

app = create_app()

# Need to listen on 0.0.0.0 to make the dev server visible to ORCID's server
app.run(debug=True, host="0.0.0.0")

from __future__ import annotations

from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField, StringField, SubmitField, FloatField, SelectField, TextAreaField, FieldList
from wtforms.validators import DataRequired, URL, Email

from .utils import validate_doi
from ..models import Experiment

class SelectOtherField(StringField):
    """ later, this could streamline the options """
    pass


class ExperimentForm(FlaskForm):
    title = StringField(
        label='Title',
        description='The name of the experiment, which should be short, easily recognizable and searchable. \
            If there is an acronym, please also provide the long name.',
        validators=[DataRequired()]
    )

    description = TextAreaField(
        label='Description',
        description='A brief description of the experiment.',
        validators=[DataRequired()],
    )

    creators = FieldList(
        unbound_field=StringField(validators=[DataRequired('Please delete unfilled spaces')]),
        label="Creators",
        description='The person(s) or organization(s) that contributed to the creation of the experiment. \
            This can be the principal investigator, hospital, university, centre, clinic, etc.',
        min_entries=1,
        max_entries=5,
        validators=[DataRequired()]
    )

    origin = SelectOtherField(
        label='Country of Origin',
        description='Country in which the experiment was primarily devised',
        validators=[],
        render_kw={
            'options-key': 'countries'
        }
    )

    contact_person = StringField(
        label='Contact Person',
        description='The person or organization responsible for the creation of the experiment.',
        validators=[DataRequired()]
    )

    contact_email = StringField(
        label='Contact Email',
        description='Email address where the the person(s) or organization(s) responsible for the creation of the \
            experiment can be contacted.',
        validators=[DataRequired(), Email()]
    )

    version = FloatField(
        label='Version',
        description='Please provide the version number, or the release point of your experiment. If you do not have \
            an existing versioning convention, we recommend the use of the following versioning convention: \
            1.0=original experiment; 1.1=minor revisions made to the experiment; 1.2=further minor revisions; \
            2.0=major/substantive changes to the experiment. For example: minor changes could include corrupted file \
            or link fixes, more description/documentation of the experiment and so on; Major changes would include \
            additional tasks included, more modalities and so on.',
    )

    privacy = SelectField(
        label='Privacy',
        description="A qualifier to describe the data protection applied to the dataset. This is relevant for clinical \
        data. Freely and publicly available experiments should be set to 'open'; experiments available to bona fide \
        researchers/clinical care professionals only should be set to 'registered'; experiments available to qualified \
        researchers approved by a committee after review of their research proposal should be set to 'controlled', \
        also known as managed or restricted access; and closed experiments, available only to researchers of the \
        project, should be set to 'closed'.",
        choices=[('Open', 'Open'), ('Registered', 'Registered'), ('Controlled', 'Controlled'), ('Private', 'Private')],
        validators=[DataRequired()]
    )

    license = SelectOtherField(
        label='License',
        description='The licence under which this experiment is shared.',
        render_kw={
            'options-key': 'licenses'
        }
    )

    keywords = FieldList(
        unbound_field=StringField(validators=[DataRequired('Please delete unfilled spaces')]),
        label='Keywords',
        description='Tags associated with the experiment, which will help in its discovery. \
        These should be well known terms by the research community.',
        validators=[DataRequired()],
        min_entries=1,
        max_entries=5
    )

    modalities = SelectOtherField(
        label='Modality',
        description='The modalities for which the experiment is designed.',
        validators=[DataRequired()],
        render_kw={
            'options-key': 'modalities'
        }
    )

    primary_software = SelectOtherField(
        label='Primary Software',
        description='the software package primarily used to develop the experiment.',
        validators=[DataRequired()],
        render_kw={
            'options-key': 'software'
        }
    )

    other_software = FieldList(
        unbound_field=StringField(),
        label="Other Software",
        description='Please provide any other software that you used to develop the experiment.',
        min_entries=1,
        max_entries=5,
    )

    primary_function = SelectOtherField(
        label='Primary Function',
        validators=[DataRequired()],
        render_kw={
            'options-key': 'functions'
        }
    )

    other_functions = FieldList(
        unbound_field=StringField(),
        label="Other Functions",
        min_entries=1,
        max_entries=5,
    )

    doi = StringField(
        label="Link to Publication (DOI)",
        validators=[validate_doi]
    )

    acknowledgements = StringField(
        label='Acknowledgements',
        description='Individuals to whom you would like to publicly express your gratitude.'
    )

    source = StringField(label='Source')
    repository = FileField("Upload zipped repository", validators=[]) # FileRequired()
    image = FileField("Upload image", validators=[
        # FileAllowed(UploadSet('images', IMAGES), 'Images only!')
    ])

    submit = SubmitField('Submit', validators=[DataRequired()])

    def get_experiment_data(self):
        data = {}
        for attribute in Experiment.required_attributes:
            entry = self.data.get(attribute)
            if entry is None:
                raise RuntimeError(f"Form entry for '{attribute}' is None")
            if isinstance(entry, list):
                data[attribute] = ", ".join(entry)
            else:
                data[attribute] = entry
        return data

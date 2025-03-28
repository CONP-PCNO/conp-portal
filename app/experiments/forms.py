import json

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    FloatField,
    TextAreaField,
    FieldList,
)
from wtforms.validators import DataRequired, Email, Optional, URL

from .data import data
from .validators import ValidDOI


class SelectOtherField(StringField):
    """later, this could streamline the options"""
    pass


class ExperimentForm(FlaskForm):

    title = StringField(
        label="Title",
        description="The name of the experiment, which should be short, easily recognizable and searchable. \
            If there is an acronym, please also provide the long name.",
        validators=[DataRequired()],
    )

    description = TextAreaField(
        label="Description",
        description="A brief description of the experiment.",
        validators=[DataRequired()],
    )

    creators = FieldList(
        unbound_field=StringField(
            validators=[DataRequired("Please delete unfilled spaces")]
        ),
        label="Creators",
        description="The person(s) or organization(s) that contributed to the creation of the experiment. \
            This can be the principal investigator, hospital, university, centre, clinic, etc.",
        min_entries=1,
        max_entries=5,
        validators=[DataRequired()],
    )

    origin = SelectOtherField(
        label="Country of Origin",
        description="Country in which the experiment was primarily devised",
        validators=[],
        render_kw={
            "data-autocomplete": json.dumps(list(data["countries"].values()))},
    )

    contact_person = StringField(
        label="Contact Person",
        description="The person or organization responsible for the creation of the experiment.",
        validators=[DataRequired()],
    )

    contact_email = StringField(
        label="Contact Email",
        description="Email address where the the person(s) or organization(s) responsible for the creation of the \
            experiment can be contacted.",
        validators=[DataRequired(), Email()],
    )

    version = FloatField(
        label="Version",
        description="Please provide the version number, or the release point of your experiment. If you do not have \
            an existing versioning convention, we recommend the use of the following versioning convention: \
            1.0=original experiment; 1.1=minor revisions made to the experiment; 1.2=further minor revisions; \
            2.0=major/substantive changes to the experiment. For example: minor changes could include corrupted file \
            or link fixes, more description/documentation of the experiment and so on; Major changes would include \
            additional tasks included, more modalities and so on.",
    )

    license = SelectOtherField(
        label="License",
        description="The license under which this experiment is shared.",
        render_kw={
            "data-autocomplete": json.dumps(list(data["licenses"].values())),
            "value": "Creative Commons Non-Commercial License (Recommended)"
        },
    )

    keywords = FieldList(
        unbound_field=StringField(
            validators=[DataRequired("Please delete unfilled spaces")]
        ),
        label="Keywords",
        description="Tags associated with the experiment, which will help in its discovery. \
        These should be well known terms by the research community.",
        validators=[DataRequired()],
        min_entries=1,
        max_entries=5,
    )

    modalities = FieldList(
        unbound_field=StringField(
            validators=[DataRequired("Please delete unfilled spaces")]
        ),
        label="Modalities",
        description="The modalities for which the experiment is designed.",
        validators=[DataRequired()],
        render_kw={"data-autocomplete": json.dumps(data["modalities"])},
        min_entries=1,
        max_entries=5,
    )

    primary_software = SelectOtherField(
        label="Primary Software",
        description="the software package primarily used to develop the experiment.",
        validators=[DataRequired()],
        render_kw={"data-autocomplete": json.dumps(data["software"])},
    )

    other_software = FieldList(
        unbound_field=StringField(),
        label="Other Software",
        description="Please provide any other software that you used to develop the experiment.",
        min_entries=1,
        max_entries=5,
        render_kw={"data-autocomplete": json.dumps(data["software"])},
    )

    primary_function = SelectOtherField(
        label="Primary Function",
        validators=[DataRequired()],
        render_kw={"data-autocomplete": json.dumps(data["functions"])},
    )

    other_functions = FieldList(
        unbound_field=StringField(),
        label="Other Functions",
        min_entries=1,
        max_entries=5,
        render_kw={"data-autocomplete": json.dumps(data["functions"])},
    )

    doi = StringField(
        label="Link to Publication (DOI)", validators=[Optional(), URL(), ValidDOI()]
    )

    acknowledgements = StringField(
        label="Acknowledgements",
        description="Individuals to whom you would like to publicly express your gratitude.",
    )

    submit = SubmitField("Submit", validators=[DataRequired()])



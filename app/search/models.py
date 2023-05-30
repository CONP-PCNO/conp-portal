import datetime as dt
from functools import lru_cache
import os
import json
import re

import fnmatch
from typing import Optional

import dateutil
import requests


@lru_cache(maxsize=1)
def _get_latest_test_results(date):
    url = "https://circleci.com/api/v1.1/" \
        + "project/github/CONP-PCNO/conp-dataset/" \
        + "latest/artifacts" \
        + "?branch=master&filter=completed"

    artifacts = requests.get(url).json()

    previous_test_results = {}
    for artifact in artifacts:
        # Merge dictionnaries together.
        previous_test_results = {
            **previous_test_results,
            **requests.get(artifact["url"]).json(),
        }

    return previous_test_results


def get_latest_test_results():
    current_date = dt.datetime.now().astimezone(tz=dateutil.tz.UTC)
    normalized_date = current_date.replace(
        # Round the date to the lowest 4hour
        hour=(current_date.hour // 4 * 4 + 1),
        minute=0,                               # range and give an extra hour gap
        second=0,                               # for tests execution.
        microsecond=0
    )

    return _get_latest_test_results(normalized_date)


class DatasetCache(object):
    def __init__(self, current_app):
        self.current_app = current_app
        dataset_cache_dir = current_app.config['DATASET_CACHE_PATH']
        if not os.path.exists(dataset_cache_dir):
            os.makedirs(dataset_cache_dir)

    @property
    def cachedDatasets(self):
        """
          Return a dict of available cached datasets
        """
        return dict(
            (f.name, f)
            for f in os.scandir(self.current_app.config['DATASET_CACHE_PATH'])
        )

    def getZipLocation(self, dataset):
        """
          1. Server checks if a zip file already exists for this version.
          2. Return zip filepath or None
        """

        datasetmeta = DATSDataset(dataset.fspath)
        zipFilename = datasetmeta.name.replace('/', '__') + '_version-' + \
            datasetmeta.version + '.tar.gz'

        # Look for the filename in the cached datasets
        cached = self.cachedDatasets.get(zipFilename)
        return cached.path if cached is not None else None


class DATSDataset(object):
    def __init__(self, datasetpath):
        """
          store the datsetopath and tries to find a DATS.json file
        """
        if not os.path.isdir(datasetpath):
            raise RuntimeError('No dataset found at {}'.format(datasetpath))

        self.datasetpath = datasetpath

        with open(self.DatsFilepath, 'r') as f:
            try:
                self.descriptor = json.load(f)
            except Exception:
                raise RuntimeError('Can`t parse {}'.format(self.DatsFilepath))

    @property
    def name(self):
        return self.datasetpath.split('conp-dataset/projects/')[-1]

    @property
    def DatsFilepath(self):
        dirs = os.listdir(self.datasetpath)
        descriptor: Optional[str] = None
        for file in dirs:
            if fnmatch.fnmatch(file.lower(), 'dats.json'):
                descriptor = os.path.join(self.datasetpath, file)
                break

        if not descriptor:
            raise RuntimeError('No DATS descriptor found')

        return descriptor

    @property
    def LogoFilepath(self):
        logopath = "app/static/img/default_dataset.jpeg"
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category') == 'logo':
                logofilename = prop.get('values').pop().get('value', '')
                if not logofilename.lower().startswith("http"):
                    logofilepath = os.path.join(
                        self.datasetpath,
                        logofilename
                    )
                    logopath = logofilepath
                else:
                    logopath = logofilename

        return logopath

    @property
    def ReadmeFilepath(self):
        dirs = os.listdir(self.datasetpath)
        readme: Optional[str] = None
        for file in dirs:
            if fnmatch.fnmatch(file.lower(), 'readme.md'):
                readme = os.path.join(self.datasetpath, file)
                break

        if not readme:
            raise RuntimeError('No Readme found')

        return readme

    @property
    def creators(self):
        creators = []
        c = self.descriptor.get('creators', '')
        if type(c) == list:
            for x in c:
                if 'name' in x:
                    creators.append(x['name'])
                if 'fullName' in x:
                    creators.append(x['fullName'])
        elif 'name' in c:
            creators.append(c['name'])
        else:
            creators.append(c)

        if len(creators) > 0:
            return creators

        return None

    @property
    def principalInvestigators(self):
        principalInvestigators = []
        creators = self.descriptor.get('creators', '')
        if type(creators) == list:
            for x in creators:
                if 'roles' in x:
                    for role in x['roles']:
                        if role['value'] == 'Principal Investigator':
                            if 'name' in x:
                                principalInvestigators.append(x['name'])
                            elif 'fullName' in x:
                                principalInvestigators.append(x['fullName'])
        elif 'roles' in creators:
            for role in creators['roles']:
                if role['value'] == 'Principal Investigator':
                    if 'name' in x:
                        principalInvestigators.append(x['name'])
                    elif 'fullName' in x:
                        principalInvestigators.append(x['fullName'])

        return principalInvestigators if len(principalInvestigators) > 0 else None

    @property
    def primaryPublications(self):
        primaryPublications = []
        publications = self.descriptor.get('primaryPublications', {})
        if type(publications) == list:
            for publi in publications:
                title = publi.get('title', '')
                if not title.endswith('.'):
                    title += '.'
                journal = publi.get('publicationVenue', '')
                if not journal.endswith('.'):
                    journal += '.'
                author = publi.get('authors', [])[0].get(
                    'fullName', '') if 'authors' in publi else ''
                if len(publi.get('authors', [])) > 1:
                    author += ' et al.'
                doi = publi.get('identifier', {}).get('identifier', '')
                primaryPublications.append(
                    {
                        'title': title,
                        'author': author,
                        'journal': journal,
                        'doi': doi
                    }
                )
        elif 'title' in publications:
            title = publications.get('title', '')
            journal = publications.get('publicationVenue', '')
            doi = publications.get('identifier', {}).get('identifier', '')
            author = publications.get('authors', [])[0].get(
                'fullName', '') if 'authors' in publications else ''
            if len(publications.get('authors', [])) > 1:
                author += ' et al.'
            primaryPublications.append(
                {
                    'title': title,
                    'author': author,
                    'journal': journal,
                    'doi': doi
                }
            )

        return primaryPublications if len(primaryPublications) > 0 else None

    @property
    def authorizations(self):
        dists = self.descriptor.get('distributions', None)
        if dists is None:
            return None

        if not type(dists) == list:
            if dists.get('@type', '') == 'DatasetDistribution':
                dist = dists
            else:
                dist = {}
        else:
            dist = dists[0]

        authorizations = dist.get('access', {}).get('authorizations', '')

        if type(authorizations) == list:
            auth = authorizations.pop().get('value', None)
        else:
            auth = None

        return "{}".format(auth)

    @property
    def origin(self):
        origin = None
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category') == 'origin':
                origin = ", ".join([x['value']
                                    for x in prop.get('values')])

        return origin

    @property
    def contacts(self):
        contacts = None
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category') == 'contact':
                contacts = ", ".join([x['value'] for x in prop.get('values')])

        return contacts

    @property
    def conpStatus(self):
        conpStatus = 'external'
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category') == 'CONP_status':
                conpStatus = prop.get('values')[0].get('value')

        return conpStatus

    @property
    def description(self):
        return self.descriptor.get('description', None)

    @property
    def fileCount(self):
        count = 0
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category') == 'files':
                for x in prop.get('values', []):
                    if isinstance(x['value'], str):
                        count += int(x['value'].replace(",", ""))
                    else:
                        count += x['value']

        return count if count > 0 else None

    @property
    def formats(self):
        formats = []
        dists = self.descriptor.get('distributions', None)
        if dists is None:
            return None

        for x in dists:
            formats += x.get('formats', [])

        return formats

    @ property
    def licenses(self):
        licenses = []
        lics = self.descriptor.get('licenses', None)
        if type(lics) == list:
            for x in lics:
                licenses.append(x.get('name'))
        else:
            if 'name' in lics:
                licenses = lics['name']
            elif '$schema' in lics:
                licenses = lics['$schema']
            elif 'dataUsesConditions' in lics:
                licenses = lics['dataUsesConditions']
            else:
                licenses = lics

        return licenses

    @ property
    def modalities(self):
        modalities = []
        for t in self.descriptor.get('types', []):
            info = t.get('information', {})
            modality = info.get('value', None)
            if modality is not None:
                modalities.append(modality)

        return modalities if len(modalities) > 0 else None

    @ property
    def keywords(self):
        keywords = []
        for t in self.descriptor.get('keywords', []):
            keyword = t.get('value', None)
            if keyword is not None:
                keywords.append(keyword)

        return keywords if len(keywords) > 0 else None

    @ property
    def size(self):
        dists = self.descriptor.get('distributions', None)
        if dists is None:
            return None

        if not type(dists) == list:
            if dists.get('@type', '') == 'DatasetDistribution':
                dist = dists
            else:
                dist = {}
        else:
            # Taking the first distribution size. (arbitrary choice)
            dist = dists[0]

        size = float(dist.get('size', 0))
        unit = dist.get('unit', {}).get('value', '')

        # Some data values from the DATS are not user friendly so
        # If size > 1000, divide n times until it is < 1000 and increment the units from the array
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
        count = 0

        while size > 1000:
            size /= 1000
            count += 1

        size = round(size, 1)
        unit = units[units.index(unit) + count]

        return "{} {}".format(size, unit)

    @ property
    def sources(self):
        dists = self.descriptor.get('distributions', None)
        if dists is None:
            return None

        if not type(dists) == list:
            if dists.get('@type', '') == 'DatasetDistribution':
                dist = dists
            else:
                dist = {}
        else:
            dist = dists[0]

        sources = dist.get('access', {}).get('landingPage', '')

        return "{}".format(sources)

    @ property
    def dimensions(self):
        dimensions = []
        for t in self.descriptor.get('dimensions', []):
            dim = t.get('name', None)
            if dim is not None:
                if dim.get('value', None) is not None:
                    dimensions.append(dim.get('value'))

        return dimensions if len(dimensions) > 0 else None

    @ property
    def isAbout(self):
        isAbout = []
        for t in self.descriptor.get('isAbout', []):
            isAb = t.get('name', None)
            if isAb is not None:
                isAbout.append(isAb)

        return isAbout if len(isAbout) > 0 else None

    @ property
    def spatialCoverage(self):
        spatialCoverage = []
        for t in self.descriptor.get('spatialCoverage', []):
            spatC = t.get('name', None)
            if spatC is not None:
                spatialCoverage.append(spatC)

        return spatialCoverage if len(spatialCoverage) > 0 else None

    @ property
    def acknowledges(self):
        acknowledges = []
        for t in self.descriptor.get('acknowledges', []):
            funders = t.get('funders', None)
            if funders is not None and type(funders) == list:
                for f in funders:
                    if f.get('name', None) is not None:
                        acknowledges.append(f.get('name', None))

        return acknowledges if len(acknowledges) > 0 else None

    @ property
    def producedBy(self):
        producedBy = []
        field_data = self.descriptor.get('producedBy', None)
        if not field_data:
            return None
        elif isinstance(field_data, str):
            producedBy.append(field_data)
        elif isinstance(field_data, dict):
            prod = field_data.get('name', None)
            if prod is not None:
                producedBy.append(prod)

        return producedBy if len(producedBy) > 0 else None

    @ property
    def subjectCount(self):
        count = 0
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category') == 'subjects':
                for x in prop.get('values', []):
                    if isinstance(x['value'], str):
                        count += int(x['value'].replace(",", ""))
                    else:
                        count += x['value']

        return count if count > 0 else None

    @ property
    def derivedFrom(self):
        derivedFrom = []
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category') == 'derivedFrom':
                for x in prop.get('values', []):
                    derivedFrom.append(x)

        return derivedFrom if len(derivedFrom) > 0 else None

    @ property
    def parentDatasetId(self):
        parentDatasetId = []
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category') == 'parent_dataset_id':
                for x in prop.get('values', []):
                    if x.get('value', None) is not None:
                        parentDatasetId.append(x.get('value'))

        return parentDatasetId if len(parentDatasetId) > 0 else None

    @ property
    def version(self):
        return self.descriptor.get('version', None)

    @property
    def dates(self):
        dates = {}
        for prop in self.descriptor.get('dates', {}):
            date = prop.get('date', '')
            date_type = prop.get('type', {}).get('value', '').title()
            dates[date_type] = date

        return dates if len(dates) > 0 else None

    @ property
    def schema_org_metadata(self):
        """ Returns json-ld metadata snippet for Google dataset search. """
        try:
            jsonld_obj = {}
            jsonld_obj["@context"] = "https://schema.org/"
            jsonld_obj["@type"] = "Dataset"
            # required fields
            jsonld_obj["name"] = self.descriptor["title"]
            jsonld_obj["description"] = self.descriptor["description"]
            jsonld_obj["version"] = self.descriptor["version"]
            licenses = []
            for license in self.descriptor["licenses"]:
                # license can be of type URL or CreativeWork
                if license["name"].startswith("http"):
                    licenses.append(license["name"])
                else:
                    license_creative_work = {}
                    license_creative_work["@type"] = "CreativeWork"
                    license_creative_work["name"] = license["name"]
                    licenses.append(license_creative_work)
            jsonld_obj["license"] = licenses
            jsonld_obj["keywords"] = [keyword["value"]
                                      for keyword in self.descriptor["keywords"]]
            creators = []
            for creator in self.descriptor["creators"]:
                if "name" in creator:
                    organization = {}
                    organization["@type"] = "Organization"
                    organization["name"] = creator["name"]
                    creators.append(organization)
                else:
                    person = {}
                    person["@type"] = "Person"
                    # all fields below are not required so we have to check if they are present
                    if "firstName" in creator:
                        person["givenName"] = creator["firstName"]
                    if "lastName" in creator:
                        person["familyName"] = creator["lastName"]
                    if "email" in creator:
                        person["email"] = creator["email"]
                    # schema.org requires 'name' or 'url' to be present for Person
                    # dats doesn't have required fields for Person,
                    # therefore in case when no 'fullName' provided or one of 'firstName' or 'lastName' is not provided
                    # we set a placeholder for 'name'
                    if "fullName" in creator:
                        person["name"] = creator["fullName"]
                    elif all(k in creator for k in ("firstName", "lastName")):
                        person["name"] = creator["firstName"] + \
                            " " + creator["lastName"]
                    else:
                        person["name"] = "Name is not provided"
                    # check for person affiliations
                    if "affiliations" in creator:
                        affiliation = []
                        for affiliated_org in creator["affiliations"]:
                            organization = {}
                            organization["@type"] = "Organization"
                            organization["name"] = affiliated_org["name"]
                            affiliation.append(organization)
                        person["affiliation"] = affiliation
                    creators.append(person)
            jsonld_obj["creator"] = creators
            return jsonld_obj

        except Exception:
            return None

    @ property
    def status(self):

        test_results = get_latest_test_results()
        tests_status = [
            results["status"]
            for test, results in test_results.items()
            if test.startswith(re.sub("/", "_", self.name) + ":")
        ]

        if tests_status == []:
            # Problem occured during the test suite.
            return "Unknown"
        if any(map(lambda x: x == "Failure", tests_status)):
            return "Broken"
        if all(map(lambda x: x == "Success", tests_status)):
            return "Working"

        return "Unknown"

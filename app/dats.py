import fnmatch
import json
import os
from typing import Optional


class DATSObject:
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

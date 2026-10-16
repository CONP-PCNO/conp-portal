import fnmatch
import json
import os

DEFAULT_LOGO = "app/static/img/default_dataset.jpeg"
DATASET_LOGOS_JSON = "app/static/datasets/dataset-logos.json"
LOGO_EXTENSIONS = (".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp")


def load_dataset_logos():
    """ Read app/static/datasets/dataset-logos.json: logos for datasets whose
        DATS.json has no logo of its own, keyed by Portal dataset id
        (e.g. "projects/PiDose").

        Returns:
            dict: {dataset_id: {"img" or "url": str, "label": str, ...}}
    """
    try:
        with open(os.path.join(os.getcwd(), DATASET_LOGOS_JSON)) as f:
            return json.load(f).get("datasets", {})
    except (OSError, ValueError):
        return {}


def dataset_logo_override(dataset_id, logos=None):
    """ The logo dataset-logos.json gives a dataset, or None when it has none.

        Returns a path under app/static/ for an "img" entry (the same kind of
        value LogoFilepath returns for a logo file in the dataset folder), or
        the URL of a "url" entry.
    """
    if not dataset_id:
        return None
    if logos is None:
        logos = load_dataset_logos()
    entry = logos.get(dataset_id)
    if not entry:
        return None
    if entry.get("img"):
        return os.path.join("app/static", entry["img"])
    return entry.get("url") or None


def resolve_dataset_logo(dataset_id, own_logo, logos=None):
    """ The logo to show for a dataset: its own DATS logo when it has one,
        else its dataset-logos.json entry, else the default image.

        own_logo may be None or DEFAULT_LOGO (both mean "no logo of its own"),
        which is what the search index stores for such datasets.
    """
    if own_logo and own_logo != DEFAULT_LOGO:
        return own_logo
    return dataset_logo_override(dataset_id, logos) or DEFAULT_LOGO


class DATSObject:
    def __init__(self, datasetpath, dataset_id=None):
        """
          store the datsetopath and tries to find a DATS.json file

          dataset_id is the Portal id ("projects/<name>"). When it is not
          given it is derived from the path for datasets under
          conp-dataset/projects/.
        """
        if not os.path.isdir(datasetpath):
            raise RuntimeError(f'No dataset found at {datasetpath}')

        self.datasetpath = datasetpath
        if dataset_id is None and 'conp-dataset/projects/' in datasetpath:
            dataset_id = 'projects/' + \
                datasetpath.split('conp-dataset/projects/')[-1].rstrip('/')
        self.dataset_id = dataset_id

        with open(self.DatsFilepath) as f:
            try:
                self.descriptor = json.load(f)
            except Exception:
                raise RuntimeError(f'Can`t parse {self.DatsFilepath}')

    @property
    def name(self):
        return self.datasetpath.split('conp-dataset/projects/')[-1]

    @property
    def DatsFilepath(self):
        dirs = os.listdir(self.datasetpath)
        descriptor: str | None = None
        for file in dirs:
            if fnmatch.fnmatch(file.lower(), 'dats.json'):
                descriptor = os.path.join(self.datasetpath, file)
                break

        if not descriptor:
            raise RuntimeError('No DATS descriptor found')

        return descriptor

    @property
    def OwnLogoFilepath(self):
        """ The dataset's own logo: the one its DATS.json names (a path in
            the dataset folder, or a URL); failing that, a logo file kept in
            the dataset folder (see RepoLogoFilepath); else None.
        """
        logopath = None
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category') == 'logo' and len(prop.get('values') or []) > 0:
                # Read the last value without removing it (this used to
                # pop(), so a second read of LogoFilepath lost the logo).
                logofilename = prop.get('values')[-1].get('value', '')
                if not logofilename:
                    continue
                if not logofilename.lower().startswith("http"):
                    logopath = os.path.join(
                        self.datasetpath,
                        logofilename
                    )
                else:
                    logopath = logofilename

        if logopath and not logopath.lower().startswith("http") \
                and not os.path.isfile(logopath):
            # DATS names a logo file that is not in the dataset folder:
            # treat it as no logo rather than fail when serving it.
            logopath = None

        return logopath or self.RepoLogoFilepath

    @property
    def RepoLogoFilepath(self):
        """ A logo file kept in the dataset folder next to DATS.json and
            README.md (logo.png, logo.jpg, logo.jpeg, logo.svg, logo.gif or
            logo.webp, any case) that DATS.json does not name; None if there
            is none.
        """
        try:
            names = sorted(os.listdir(self.datasetpath))
        except OSError:
            return None
        for name in names:
            stem, ext = os.path.splitext(name)
            if stem.lower() == "logo" and ext.lower() in LOGO_EXTENSIONS:
                path = os.path.join(self.datasetpath, name)
                # isfile follows symlinks, so a DataLad file whose content
                # has not been fetched is skipped.
                if os.path.isfile(path):
                    return path
        return None

    @property
    def LogoFilepath(self):
        """ The dataset's own logo (named in DATS.json, or a logo file in
            the dataset folder); failing that, its entry in
            app/static/datasets/dataset-logos.json; failing that, the
            default image. The dataset's own logo always wins.
        """
        return resolve_dataset_logo(self.dataset_id, self.OwnLogoFilepath)

    @property
    def ReadmeFilepath(self):
        dirs = os.listdir(self.datasetpath)
        readme: str | None = None
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
        if isinstance(c, list):
            for x in c:
                print(x)
                if x.get('name', ''):
                    creators.append(x['name'])
                elif x.get('fullName', ''):
                    creators.append(x['fullName'])
                elif x.get('firstName', ''):
                    first_name = x['firstName']
                    last_name = x.get('lastName', '')
                    creators.append(f'{first_name} {last_name}')
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
        if isinstance(creators, list):
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
        if isinstance(publications, list):
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
    def privacy(self):
        return self.descriptor.get("privacy", None)

    @property
    def authorizations(self):
        dists = self.descriptor.get('distributions', None)
        if dists is None:
            return None

        if not isinstance(dists, list):
            if dists.get('@type', '') == 'DatasetDistribution':
                dist = dists
            else:
                dist = {}
        else:
            dist = dists[0]

        authorizations = dist.get('access', {}).get('authorizations', '')

        if isinstance(authorizations, list) and len(authorizations) > 0:
            auth = authorizations.pop().get('value', None)
        else:
            auth = None

        return f"{auth}"

    @property
    def origin(self):
        origin = []
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category').startswith('origin_'):
                key = prop.get('category').replace('origin_', '').capitalize()
                origin.append(
                    f"{key}: " + ", ".join([x['value'] for x in prop.get('values')])
                )
        return ", ".join(origin)

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

    @property
    def licenses(self):
        licenses = []
        lics = self.descriptor.get('licenses', None)
        if isinstance(lics, list):
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

    @property
    def modalities(self):
        modalities = []
        for t in self.descriptor.get('types', []):
            info = t.get('information', {})
            modality = info.get('value', None)
            if modality is not None:
                modalities.append(modality)

        return modalities if len(modalities) > 0 else None

    @property
    def keywords(self):
        keywords = []
        for t in self.descriptor.get('keywords', []):
            keyword = t.get('value', None)
            if keyword is not None:
                keywords.append(keyword)

        return keywords if len(keywords) > 0 else None

    @property
    def size(self):
        dists = self.descriptor.get('distributions', None)
        if dists is None:
            return None

        if not isinstance(dists, list):
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

        return f"{size} {unit}"

    @property
    def sources(self):
        dists = self.descriptor.get('distributions', None)
        if dists is None:
            return None

        if not isinstance(dists, list):
            if dists.get('@type', '') == 'DatasetDistribution':
                dist = dists
            else:
                dist = {}
        else:
            dist = dists[0]

        sources = dist.get('access', {}).get('landingPage', '')

        return f"{sources}"

    @property
    def dimensions(self):
        dimensions = []
        for t in self.descriptor.get('dimensions', []):
            dim = t.get('name', None)
            if dim is not None:
                if dim.get('value', None) is not None:
                    dimensions.append(dim.get('value'))

        return dimensions if len(dimensions) > 0 else None

    @property
    def isAbout(self):
        isAbout = []
        for t in self.descriptor.get('isAbout', []):
            isAb = t.get('name', None)
            if isAb is not None:
                isAbout.append(isAb)

        return isAbout if len(isAbout) > 0 else None

    @property
    def spatialCoverage(self):
        spatialCoverage = []
        for t in self.descriptor.get('spatialCoverage', []):
            spatC = t.get('name', None)
            if spatC is not None:
                spatialCoverage.append(spatC)

        return spatialCoverage if len(spatialCoverage) > 0 else None

    @property
    def acknowledges(self):
        acknowledges = []
        for t in self.descriptor.get('acknowledges', []):
            funders = t.get('funders', None)
            if funders is not None and isinstance(funders, list):
                for f in funders:
                    if f.get('name', None) is not None:
                        acknowledges.append(f.get('name', None))

        return acknowledges if len(acknowledges) > 0 else None

    @property
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

    @property
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

    @property
    def derivedFrom(self):
        derivedFrom = []
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category') == 'derivedFrom':
                for x in prop.get('values', []):
                    derivedFrom.append(x)

        return derivedFrom if len(derivedFrom) > 0 else None

    @property
    def parentDatasetId(self):
        parentDatasetId = []
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category') == 'parent_dataset_id':
                for x in prop.get('values', []):
                    if x.get('value', None) is not None:
                        parentDatasetId.append(x.get('value'))

        return parentDatasetId if len(parentDatasetId) > 0 else None

    @property
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

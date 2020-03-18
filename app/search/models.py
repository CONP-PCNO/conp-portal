import os
import json
import fnmatch

class DATSDataset(object):
    def __init__(self, datasetpath):
        """
          store the datsetopath and tries to find a DATS.json file
        """
        if not os.path.isdir(datasetpath):
            raise 'No dataset found at {}'.format(datasetpath)
        self.datasetpath = datasetpath

        with open(self.DatsFilepath, 'r') as f:
            try:
                self.descriptor = json.load(f)
            except Exception as e:
                raise 'Can`t parse {}'.format(self.DatsFilepath)

    @property
    def DatsFilepath(self):
        dirs = os.listdir(self.datasetpath)
        for file in dirs:
            if fnmatch.fnmatch(file.lower(), 'dats.json'):
                descriptor = os.path.join(self.datasetpath, file)
                break

        if descriptor == None:
            raise 'No DATS descriptor found'

        return descriptor


    @property
    def LogoFilepath(self):
        logopath = "app/static/img/default_dataset.jpeg"
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category') == 'logo':
                logofilename = prop.get('values').pop().get('value', '')
                logofilepath = os.path.join(
                    self.datasetpath,
                    logofilename
                )
                if os.path.isfile(logofilepath):
                    logopath = logofilepath

        return logopath



    @property
    def authors(self):
        authors = []
        creators = self.descriptor.get('creators', '')
        if type(creators) == list:
            for x in creators:
                if 'name' in x:
                    authors.append(x['name'])
                if 'fullname' in x:
                    authors.append(x['fullname'])
        elif 'name' in creators:
            authors.append(creators['name'])
        else:
            authors.append(creators)

        return ", ".join(authors) if len(authors) > 0 else None


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
        formats = None
        dists = self.descriptor.get('distributions', None)
        if dists is None:
            return None

        if not type(dists) == list:
            if dists.get('@type', '') == 'DatasetDistribution':
                formats = ", ".join([x['description'] for x in dists.get('formats', [])])
        else:
            formats = ", ".join([", ".join(x['formats']) for x in dists])

        return formats

    @property
    def licenses(self):
        licenseString = self.descriptor.get('licenses', 'None')
        licenses = licenseString
        if type(licenseString) == list:
            licenses = ", ".join([x['name'] for x in licenseString])
        else:
            if 'name' in licenseString:
                licenses = licenseString['name']
            elif '$schema' in licenseString:
                licenses = licenseString['$schema']
            elif 'dataUsesConditions' in licenseString:
                licenses = licenseString['dataUsesConditions']
            else:
                licenses = licenseString

        return licenses


    @property
    def modalities(self):
        modalities = []
        for t in self.descriptor.get('types', []):
            info = t.get('information', {})
            modality = info.get('value', None)
            if modality is not None:
                modalities.append(modality)

        return ", ".join(modalities) if len(modalities) > 0 else None

    @property
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
        
        size = dist.get('size', 0)
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


    @property
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
    def version(self):
        return self.descriptor.get('version', None)


    @property
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
            jsonld_obj["keywords"] = [keyword["value"] for keyword in self.descriptor["keywords"]]
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
                        person["name"] = creator["firstName"] + " " + creator["lastName"]
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

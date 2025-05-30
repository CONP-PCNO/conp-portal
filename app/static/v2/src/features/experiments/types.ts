export type ItemsPerPageType = 5 | 10 | 15 | 20;

export interface Experiment {
  id: number;
  title: string;
  description: string;
  creators: string[];
  origin: string;
  contactPerson: string;
  contactEmail: string;
  version: number;
  dateAdded: Date;
  dateUpdated: Date;
  privacy: string;
  license: string;
  keywords: string[];
  modalities: string[];
  primarySoftware: string;
  otherSoftware: string[];
  primaryFunction: string;
  otherFunctions: string[];
  primaryPublications: { 
    title: string; 
    author: string; 
    journal: string; 
    doi: string;
  }[];
  doi: string;
  acknowledgements: string;
  source: string;
  views: number;
  downloads: number;
  repositoryFile: string;
  repositoryFileCount: number;
  repositorySize: string;
  imageFile?: string;
  remoteUrl: string;
}

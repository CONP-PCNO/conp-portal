export interface Experiment {
  id: number;
  title: string;
  description: string;
  creators: string[];
  origin: string;
  contact_person: string;
  contact_email: string;
  version: number;
  date_added: Date;
  date_updated: Date;
  privacy: string;
  license: string;
  keywords: string[];
  modalities: string[];
  primary_software: string;
  other_software: string[];
  primary_function: string;
  other_functions: string[];
  doi: string;
  acknowledgements: string;
  source: string;
  views: number;
  downloads: number;
  repository_file: string;
  image_file: string;
}

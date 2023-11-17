import React from 'react';
import ReactMarkdown from 'react-markdown';
import { ExperimentCard } from '../components/ExperimentCard';
import { Experiment } from '../types';

const additionalProps: Array<keyof Experiment> = [
  'keywords',
  'title',
  'license',
  'creators',
  'origin',
  'contactPerson',
  'contactEmail',
  'privacy',
  'otherSoftware',
  'otherFunctions',
  'acknowledgements',
  'source',
  'version',
  'modalities',
  'repositorySize',
  'repositoryFileCount',
  'source',
  'acknowledgements',
];

export interface ExperimentPageProps {
  experiment: Experiment;
  downloadLink: string;
  readme: string;
}

function  handleKeywordClick (keyword) {
  const encodedKeyword = encodeURIComponent(keyword.trim());
  const searchUrl = `/experiments/search`;
  window.location.href = searchUrl;
}

export const ExperimentPage = ({ experiment, downloadLink, readme }: ExperimentPageProps) => {
  return (
    <div>
      <ExperimentCard
         experiment={experiment}
         downloadLink={downloadLink} />
        <div className="d-flex flex-column p-4">
          <div className="py-2">
          <strong>Keywords:</strong>

          {experiment["keywords"].toString().split(',').map((keyword) => (
              <span className="mr-1" key={keyword.trim()}><a className='badge badge-info' onClick={() => handleKeywordClick(keyword)}>{keyword.trim()}</a></span>
              // <KeywordLink key={keyword.trim()} keyword={keyword} />
          ))}
          </div>
          <h5><strong>{experiment["title"]}</strong></h5>    
          <div className="py-2">
              <strong>Creators: </strong>
              {experiment["creators"].map((creator, index, arr) => (
                <>
                  {creator}
                  {index !== arr.length - 1 ? ', ' : ''}
                </>
              ))}
          </div> 
          <div className="py-1">
              <strong>Contact: </strong>
              {experiment["contactPerson"]}
          </div>
          <div className="py-1">
              <strong>Licenses: </strong>
              {experiment["license"]}
          </div>
          <div className="py-1">
              <strong>Version: </strong>
              {experiment["version"]}
          </div>
          <div className="py-1">
              <strong>Modalities: </strong>
              {experiment["modalities"].map((modalities) => (
                  <span className="mr-1" key={modalities}><a className='badge badge-info'>{modalities}</a></span>
              ))}
          </div>
          <div className="py-1">
              <strong>Size: </strong>
              {experiment["repositorySize"]}
          </div>
          <div className="py-1">
              <strong>No of Files: </strong>
              {experiment["repositoryFileCount"]}
          </div>
          <div className="py-1">
              <strong>Source: </strong>
              <a href={experiment["source"]} target="_blank" rel="noopener noreferrer">
                  {experiment["source"]}
              </a>
          </div>
        </div>
        <div className="d-flex flex-column p-4">
            <h5><strong>Description:</strong></h5>
            <div className="py-1">{experiment["description"]}</div>
        </div>

        {readme !== "" && (
          <>
            <div className="d-flex flex-column p-2">
              <h2>Experiment README Information</h2>
            </div>
            <div className="card">
              <div className="card-header">README.md</div>
              <div className="card-body">
                <ReactMarkdown>{readme}</ReactMarkdown>
              </div>
            </div>
          </>
        )}
    </div>
  );
};


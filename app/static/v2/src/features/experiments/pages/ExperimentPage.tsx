import React, { useEffect }  from 'react';
import ReactMarkdown from 'react-markdown';
import { ExperimentCard } from '../components/ExperimentCard';
import { Experiment } from '../types';
import "./ExperimentPage.css";

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
  'primaryPublications',
  'acknowledgements',
  'source',
  'version',
  'modalities',
  'repositorySize',
  'repositoryFileCount',
  'repositoryFile',
  'source',
  'acknowledgements'
];

export interface ExperimentPageProps {
  experiment: Experiment;
  downloadLink: string;
  readme: string;
}

function  handleKeywordClick (keyword) {
  const encodedKeyword = encodeURIComponent(keyword.trim());
  const searchUrl = `/experiments/search?keyword=${encodedKeyword}`;
  window.location.href = searchUrl;
}

const downloadExperimentMetadata = (event, experiment) => {
  event.preventDefault();

  const fileUrl = `${window.origin}/download_metadata_experiment?experiment=${experiment.id}`;

  const link = document.createElement("a");
  link.href = fileUrl;
  link.download = experiment['title'].replace(/\s+/g, "_") + ".dats.json"; // Nom propre du fichier
  link.click();
};

export const ExperimentPage = ({ experiment, downloadLink, readme }: ExperimentPageProps) => {
  
  useEffect(() => {
    console.log("Additional Props:", additionalProps);
    console.log("Experiment Data:", experiment);
  }, [experiment]);

  return (
    <div>
      <ExperimentCard
         experiment={experiment}
         downloadLink={downloadLink} />
        <div className="d-flex flex-column p-4">
          <div className="py-2">
          <strong>Keywords:</strong>

          {experiment["keywords"].toString().split(',').map((keyword) => (
              <span className="mr-1" key={keyword.trim()}><a className='badge badge-info' onClick={() => handleKeywordClick(keyword)} style={{ cursor: 'pointer' }}>{keyword.trim()}</a></span>
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
                  <span className="mr-1" key={modalities}><a className='badge badge-info' onClick={() => handleKeywordClick(modalities)} style={{ cursor: 'pointer' }}>{modalities}</a></span>
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
          {experiment["primaryPublications"].length > 0 && (
            <div className="py-1" style={{ marginBottom: 0 }}>
              <strong>
                {experiment["primaryPublications"].length > 1 ? "Primary Publications: " : "Primary Publication: "}
              </strong>
              {experiment["primaryPublications"][0].title} {experiment["primaryPublications"][0].author} {" "}
              <em>{experiment["primaryPublications"][0].journal}</em>
              {experiment["primaryPublications"][0].doi && (
                <a target="_blank" rel="noopener noreferrer" href={experiment["primaryPublications"][0].doi}>
                  {experiment["primaryPublications"][0].doi}
                </a>
              )}
              {experiment["primaryPublications"].length > 1 && (
                <ul style={{ listStyleType: "none", paddingLeft: 0, marginBottom: 0 }}>
                  {experiment["primaryPublications"].slice(1).map((pub, index) => (
                    <li key={index} style={{ marginBottom: 0 }}>
                      {pub.title} {pub.author} <em>{pub.journal}</em>
                      {pub.doi && (
                        <a target="_blank" rel="noopener noreferrer" href={pub.doi}>
                          {pub.doi}
                        </a>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
          <div className="py-1">
              <strong>Browse on GitHub: </strong>
              <a href={experiment["remoteUrl"]} target="_blank" rel="noopener noreferrer">
                  {experiment["remoteUrl"]}
              </a>
          </div>
          <div className="py-1">
              <strong>Source: </strong>
              <a href={experiment["source"]} target="_blank" rel="noopener noreferrer">
                  {experiment["source"]}
              </a>
          </div>
          <div className="py-1">
              <strong>Metadata file: </strong>
              <a href="#" onClick={(event) => downloadExperimentMetadata(event, experiment)}>
                DATS.json
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


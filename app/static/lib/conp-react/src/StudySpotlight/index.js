import React from "react";

const StudySpotlight = (props) => {
  const studies = [
    {
      title: "PREVENT-AD Datasets",
      logo: "/dataset_logo?id=projects/preventad-registered",
      description: <>
        <p>
          The PREVENT-AD (Pre-symptomatic Evaluation of Experimental or
          Novel Treatments for Alzheimer's Disease) cohort is composed of
          cognitively healthy participants over 55 years old, at risk of
          developing Alzheimer's Disease (AD) as their parents and/or
          siblings were/are affected by the disease. These ‘at-risk’
          participants have been followed for a naturalistic study of the
          presymptomatic phase of AD since 2011 using multimodal
          measurements of various disease indicators. One clinical trial
          intended to test a pharmaco-preventive agent has also been
          conducted.
        </p>
      </>,
      buttons: [
        {
          label: 'Open Dataset',
          link: '/dataset?id=projects/preventad-open',
        },
        {
          label: 'Open Dataset (BIDS)',
          link: '/dataset?id=projects/preventad-open-bids',
        },
        {
          label: 'Registered Dataset',
          link: '/dataset?id=projects/preventad-registered',
        },
      ],
      authors: "StoP-AD Center - Douglas Mental Health University Institute"
    },
    {
      title: "RECOVER: REaching patients with a COncussion Visiting the Emergency Room to enhance care",
      logo: "https://www.braincode.ca/sites/default/files/dr014_CON_logo.png",
      description: <>
        <p>
        The Concussion Ontario Network: Neuroinformatics to Enhance Clinical care and Translation (CONNECT) 
        is a collaborative network of 10 clinical sites across Ontario that aim to ensure new knowledge of concussion 
        is translated into better diagnosis and care for the benefit of all Ontarians. 
        Given that the pathophysiology of concussion is largely unknown, a systems approach could provide 
        a holistic framework for the study of concussion. 
        Therefore, the overall purpose of the RECOVER pilot study is to demonstrate the ability to characterize 
        ultra-early acute concussion in adults using a harmonized multi-scale system approach by collecting data 
        that are potential predictors of persistent post-concussion symptoms (PPCS) over a 12- week period.
        </p>
      </>,
      buttons: [
        {
          label: 'Registered Dataset',
          link: '/dataset?id=projects/braincode_CONNECT_RECOVER',
        }
      ],
      authors: "Ontario Brain Institute"
    },
    {
      title: "MICA-MICs: a dataset for Microstructure-Informed Connectomics",
      logo: "/dataset_logo?id=projects/mica-mics",
      description: <>
        <p>
        The MICA-MICs dataset leverages the rich descriptions of brain structure and function offered by MRI 
        to further our understanding of human brain organization across modalities and spatial scales. 
        MICA-MICs is a dataset for microstructure-informed connectomics providing raw and fully processed 
        multimodal neuroimaging data acquired in 50 healthy control participants at an MRI field strength of 3T. 
        Modalities include high-resolution anatomical (T1-weighted), microstructurally-sensitive (quantitative T1), 
        diffusion-weighted, and resting-state functional imaging. 
        We additionally provide users with ready-to-use connectomes built across multiple parcellation schemes based 
        on histology (e.g. Von Economo), sulco-gyral landmarks (e.g. Desikan-Killiany), and function (e.g. Schaefer atlases), 
        for a total of 18 different parcellations of varying spatial scale.
        </p>
      </>,
      buttons: [
        {
          label: 'Open Dataset',
          link: '/dataset?id=projects/mica-mics',
        }
      ],
      authors: "Jessica Royer, Raul Rodriguez-Cruces, Shahin Tavakol et al."
    },
    {
      title: "Adolescent Brain Development",
      logo: "/dataset_logo?id=projects/AdolescentBrainDevelopment",
      description: <>
        <p>
          Children were recruited between 6 and 13 years of age. 
          All data was acquired at the Alberta Children's Hospital on a GE 3T Discovery MR750w system. 
          Participants were asked to return after 2 years to provide a longitudinal time point with the same scan protocol and cognitive examination battery. 
          Some participants returned for a third visit, as they reached 4 years from their initial time point while the study was still actively acquiring data. 
          A battery of cognitive examinations was also collected during study visits.
        </p>
      </>,
      buttons: [
        {
          label: 'Open Dataset',
          link: '/dataset?id=projects/AdolescentBrainDevelopment',
        },
      ],
      authors: "Catherine Lebel - Developmental Neuroimaging Lab, University of Calgary"
    },
    {
      title: "Calgary Preschool MRI Dataset",
      logo: "/dataset_logo?id=projects/Calgary-Preschool-MRI-Dataset",
      description: <>
        <p>
          The Calgary Preschool MRI Dataset, produced by the Developmental Neuroimaging Lab 
          at the University of Calgary, captures brain structure and function in 143 young 
          children aged 2–13 through a number of MRI modalities: T1w, T2w, DWI, resting-state 
          fMRI, ihMT, and ASL. The data are designed to chart typical neurodevelopment and 
          provide a normative baseline for identifying atypical development in pediatric 
          clinical populations. The dataset is openly available through the CONP Portal 
          via DataLad and cognitive assessment data are available on request.
        </p>
      </>,
      buttons: [
        {
          label: 'Open Dataset',
          link: '/dataset?id=projects/Calgary-Preschool-MRI-Dataset',
        },
      ],
      authors: "Developmental Neuroimaging Lab, University of Calgary"
    },    
    {
      title: "Calgary Campinas Brain MRI Dataset",
      logo: "/dataset_logo?id=projects/calgary-campinas",
      description: <>
        <p>
          The Calgary-Campinas-359 dataset is a large, open brain MRI collection acquired 
          across multiple vendors and field strengths, providing raw k-space and reconstructed 
          image data from 359 healthy adult participants. Designed to support MRI reconstruction 
          research and evaluation of skull-stripping methods, it is available through the CONP Portal.
        </p>
      </>,
      buttons: [
        {
          label: 'Open Dataset',
          link: '/dataset?id=projects/calgary-campinas',
        },
      ],
      authors: "Roberto Souza, Richard Frayne, Leticia Rittner"
    },
  ];


  return (
    <div className="card-description">
      <h3 className="card-description-title">STUDY SPOTLIGHT</h3>
      <hr />
      <div id="study-spotlight-carousel" className="carousel slide" data-bs-ride="carousel" data-bs-interval="10000">
        <ol className="carousel-indicators">
          {studies.map((study, i) =>
            <li
              data-bs-target="#study-spotlight-carousel"
              data-bs-slide-to={i}
              className={i === 0 ? "active" : ""}
            ></li>
          )}
        </ol>
        <div className="carousel-inner">
          {studies.map((study, i) =>
            <div className={i === 0 ? "carousel-item active" : "carousel-item"}>
              <div className="card-description-text">
                <div className="card-img d-flex justify-content-center">
                  {study.logo && <img style={{ maxHeight: '220px', maxWidth: '250px' }} alt="Project image" className="img-fluid" src={study.logo} />}
                </div>
                <p className="card-description-subtitle">{study.title}</p>
                {study.description}
              </div>
              <div className="d-flex mt-4 justify-content-around">
                {study.buttons.map((button) =>
                  <div>
                    <a href={button.link}>
                      <button className="btn btn-outline-secondary" type="button">
                        {button.label}
                      </button>
                    </a>
                  </div>
                )}
              </div>
              <div className="card-description-subtitle">
                <p>Authors: {study.authors}</p>
              </div>
            </div>
          )}
        </div>
        <button className="carousel-control-prev" type="button" data-bs-target="#study-spotlight-carousel" data-bs-slide="prev">
          <span className="carousel-control-prev-icon" aria-hidden="true"></span>
          <span className="sr-only">Previous</span>
        </button>
        <button className="carousel-control-next" type="button" data-bs-target="#study-spotlight-carousel" data-bs-slide="next">
          <span className="carousel-control-next-icon" aria-hidden="true"></span>
          <span className="sr-only">Next</span>
        </button>
      </div>
    </div>
  );
};

export default StudySpotlight;

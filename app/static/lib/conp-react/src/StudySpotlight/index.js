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
      title: "Calgary Campinas Brain MRI Dataset",
      logo: "/dataset_logo?id=projects/calgary-campinas",
      description: <>
        <p>
          The dataset is currently composed of 3D,
          T1-weighted reconstructed brain MR images and segmentation masks for certain structures.
          It also has brain MR raw data (i.e., k-space).
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
    <div class="card-description">
      <h3 class="card-description-title">STUDY SPOTLIGHT</h3>
      <hr />
      <div id="study-spotlight-carousel" class="carousel slide" data-ride="carousel" data-interval="10000">
        <ol class="carousel-indicators">
          {studies.map((study, i) =>
            <li
              data-target="#study-spotlight-carousel"
              data-slide-to={i}
              class={i === 0 ? "active" : ""}
            ></li>
          )}
        </ol>
        <div class="carousel-inner">
          {studies.map((study, i) =>
            <div class={i === 0 ? "carousel-item active" : "carousel-item"}>
              <div class="card-description-text">
                <div class="card-img d-flex justify-content-center">
                  <img
                    alt="Project image"
                    class="img-fluid"
                    src={study.logo}
                  />
                </div>
                <p class="card-description-subtitle">{study.title}</p>
                {study.description}
              </div>
              <div class="d-flex mt-4 justify-content-around">
                {study.buttons.map((button) => 
                  <div>
                    <a href={button.link}>
                      <button class="btn btn-outline-secondary" type="button">
                        {button.label}
                      </button>
                    </a>
                  </div>
                )}
              </div>
              <div class="card-description-subtitle">
                <p>Authors: {study.authors}</p>
              </div>
            </div> 
          )}
        </div>
        <button class="carousel-control-prev" type="button" data-target="#study-spotlight-carousel" data-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="sr-only">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-target="#study-spotlight-carousel" data-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="sr-only">Next</span>
        </button>
      </div>


      
    </div>
  );
};

export default StudySpotlight;

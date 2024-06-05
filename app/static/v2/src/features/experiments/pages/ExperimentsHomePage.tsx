import React from 'react';

export interface ExperimentsHomePageProps {
  searchPageUrl: string;
  submitPageUrl: string;
}

export const ExperimentsHomePage = ({ searchPageUrl, submitPageUrl }: ExperimentsHomePageProps) => {
  return (
    <div className="d-flex h-100 w-100 align-items-center justify-content-center">
      <div className="jumbotron bg-white text-center">
        <div className="container">
          <h1 className="jumbotron-heading display-5">Welcome to the Experiments Portal</h1>
          <i className="fa fa-desktop fa-5x"></i>
          <div>
            <p className="lead text-muted">
              CONP Experiments is an open-source experiment-sharing platform for multimodal, software-independent,
              functional neuroimaging tasks within the infrastructure of the Canadian Open Neuroscience Platform (CONP)
              Portal.
            </p>
          </div>
          <hr className="my-4" />
          <div className="row">
            <div className="col-lg-6">
              <a className="btn btn-primary text-uppercase font-weight-bold my-1" href={searchPageUrl}>
                Search Experiments
              </a>
            </div>
            <div className="col-lg-6">
              <a className="btn btn-secondary text-uppercase font-weight-bold my-1" href={submitPageUrl}>
                Submit New Experiment
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

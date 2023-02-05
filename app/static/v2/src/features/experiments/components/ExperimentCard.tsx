import React from 'react';

import brain from '@/assets/brain.gif';

interface ExperimentCardProps {
  titleLink?: boolean;
  imageUrl?: string;
}

export const ExperimentCard = ({ titleLink, imageUrl }: ExperimentCardProps) => {
  return (
    <div className="card container-fluid">
      <div className="row">
        <div className="col col-sm-2 d-flex flex-column justify-content-center">
          <div className="container-fluid p-2">
            <img className="animated-gif img-fluid" alt="experiment image" src={imageUrl ?? brain} />
          </div>
        </div>
      </div>
      <div className="col col-lg-7 card-body d-flex p-2">
      </div>
    </div>
  );
};

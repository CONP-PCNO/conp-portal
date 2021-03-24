import React from "react";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faDownload } from '@fortawesome/free-solid-svg-icons'

const DownloadsIcon = (props) => {

    return (
        <div className="d-flex flex-column align-items-center mx-2" >
            <FontAwesomeIcon icon={faDownload} color="dimgray" size="md" />
            {props.downloads}
        </div>

    );
};

export default DownloadsIcon;

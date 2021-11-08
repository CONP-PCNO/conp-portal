import React, { useState, useEffect } from "react";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faDownload } from '@fortawesome/free-solid-svg-icons'

const DownloadsIcon = (props) => {

    const [downloads, setDownloads] = useState()
    const [isLoading, setIsLoading] = useState(true)
    const url = props.type === "dataset" ? `/analytics/datasets/downloads?id=${props.id}` : `/analytics/pipelines/views?id=${props.id}`

    useEffect(() => {
        fetchDownloads();
    }, [])

    useEffect(() => {
        if (!isLoading && downloads) {
            setIsLoading(false)
        }
    }, [downloads])

    const fetchDownloads = () => {

        try {
            fetch(url)
                .then(res => res.json())
                .then(json => setDownloads(json[0]))
                .then(setIsLoading(false));
        } catch (err) {
            console.error(err);
        }

    };

    return (
        <div className="d-flex flex-column align-items-center mx-2" >
            <FontAwesomeIcon icon={faDownload} color="dimgray" size="md"/>
            {(!!downloads && downloads.nb_hits || "NA")}
        </div>

    );
};

export default DownloadsIcon;

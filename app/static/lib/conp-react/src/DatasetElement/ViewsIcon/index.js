import React, { useState, useEffect } from "react";

import LoadingSpinner from "../../charts/LoadingSpinner"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faEye } from '@fortawesome/free-solid-svg-icons'

const ViewsIcon = (props) => {

    const [views, setViews] = useState([])
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        fetchViews();
    }, [])

    const fetchViews = async () => {

        try {
            fetch(`/analytics/datasets/views?id=${props.datasetId}`)
                .then(res => res.json())
                .then(json => {
                    console.log(json)
                    return setViews(json)
                })
                .then(
                    setIsLoading(false)
                );

        } catch (err) {
            console.error(err);
        }

    };

    return (
        isLoading ? <LoadingSpinner /> :
            <div className="d-flex flex-column align-items-center mx-2" >
                <FontAwesomeIcon icon={faEye} color="dimgray" size="md" />
                7
            </div>

    );
};

export default ViewsIcon;

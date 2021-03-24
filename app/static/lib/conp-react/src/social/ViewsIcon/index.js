import React, { useState, useEffect } from "react";

import LoadingSpinner from "../../charts/LoadingSpinner"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faEye } from '@fortawesome/free-solid-svg-icons'

const ViewsIcon = (props) => {

    const [views, setViews] = useState()
    const [isLoading, setIsLoading] = useState(true)
    const url = props.type === "dataset" ? `/analytics/datasets/views?id=${props.id}` : `/analytics/pipelines/views?id=${props.id}`

    useEffect(() => {
        fetchViews();
    }, [])

    useEffect(() => {
        if (!isLoading && views) {
            setIsLoading(false)
        }
    }, [views])

    const fetchViews = () => {

        try {
            fetch(url)
                .then(res => res.json())
                .then(json => setViews(json[0]))
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
                {!!views && views.nb_hits}
            </div>

    );
};

export default ViewsIcon;

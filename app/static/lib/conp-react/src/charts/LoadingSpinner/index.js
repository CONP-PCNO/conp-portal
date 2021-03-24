const LoadingSpinner = (props) => {

    return (
        <div className="d-flex justify-content-center align-items-center w-100 h-100">
            <div className="spinner-grow text-info" role="status">
                <span className="sr-only">Loading...</span>
            </div>
        </div>
    )
}

export default LoadingSpinner
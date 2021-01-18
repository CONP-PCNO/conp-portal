const ContextMenu = (props) => {

    const { url, style, show } = props.options

    console.log(style);
    console.log(url);

    return (
        <div className="dropdown" style={style}>
            <ul className={"dropdown-menu" + (show ? " show" : "")} role="menu" aria-labelledby="dropdownMenu">
                <li><a className="dropdown-item" href={url}>View Datasets</a></li>
                <li><a className="dropdown-item" href={url} target='_blank'>View Datasets in New Tab</a></li>
            </ul>
        </div>
    )
}

export default ContextMenu
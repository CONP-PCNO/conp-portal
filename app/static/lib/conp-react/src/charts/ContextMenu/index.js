import { useCallback, useEffect, useState } from 'react'

const ContextMenu = (props) => {

    const [dimensions, setDimensions] = useState(null);
    const [style, setStyle] = useState(null);


    const callBackRef = useCallback(domNode => {
        if (domNode) {
            setDimensions(domNode.getBoundingClientRect());
        }
    }, []);

    console.log("1", props.options.style);
    //console.log(props.options.url);
    console.log("2", dimensions);

    useEffect(() => {
        props.options.style && dimensions && setStyle(
            {
                ...props.options.style,
                top: props.options.style.top - dimensions.top - 80,
                left: props.options.style.left - dimensions.left
            }
        )
    }, [props.options.style])

    console.log("3", style)

    return (
        <div ref={callBackRef} className="dropdown" style={style}>
            <div className={"dropdown-menu" + (props.options.show ? " show" : "")} role="menu" aria-labelledby="dropdownMenu">
                <span className="dropdown-item-text"><b>{props.options.title}</b></span>
                <div className="dropdown-divider"></div>
                <a className="dropdown-item" href={props.options.url}>{props.options.actionText}</a>
                <a className="dropdown-item" href={props.options.url} target='_blank'>{props.options.actionText} in New Tab</a>
            </div>
        </div>
    )
}

export default ContextMenu
import { useCallback, useEffect, useState } from 'react'

const ContextMenu = (props) => {

    const [dimensions, setDimensions] = useState(null);
    const [style, setStyle] = useState(null);


    const callBackRef = useCallback(domNode => {
        if (domNode) {
            setDimensions(domNode.getBoundingClientRect());
        }
    }, []);

    useEffect(() => {
        props.options.style && dimensions && setStyle(
            {
                ...props.options.style,
                top: props.options.style.top - dimensions.top - 80,
                left: props.options.style.left - dimensions.left
            }
        )
    }, [dimensions, props.options.style])

    useEffect(() => {
        // $(".dropdown-menu").toggle()
    }, [props.options.style])

    return (
        <div ref={callBackRef} className="dropdown" style={style}>
            <div className="dropdown-menu">
                <span className="dropdown-item-text"><b>{props.options.title}</b></span>
                <div className="dropdown-divider"></div>
                <a className="dropdown-item" href={props.options.url}>{props.options.actionText}</a>
                <a className="dropdown-item" href={props.options.url} target='_blank' rel="noreferrer">{props.options.actionText} in New Tab</a>
            </div>
        </div>
    )
}

export default ContextMenu
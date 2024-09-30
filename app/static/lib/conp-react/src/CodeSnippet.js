import React, { useState } from "react";
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCopy } from '@fortawesome/free-regular-svg-icons';
import { faCheck } from '@fortawesome/free-solid-svg-icons';

const CodeSnippet = ({code}) => {
  const [showCopyIcon, setShowCopyIcon] = useState(true);
  const [showCheckIcon, setShowCheckIcon] = useState(false);

  const handleCopyToClipboard = e => {
    setShowCopyIcon(false)
    setShowCheckIcon(true)
    setTimeout(() => {
      setShowCopyIcon(true)
      setShowCheckIcon(false)
    }, 1000)
  }

  const formatCode = (code) => code.map((line) => <>{line}<br/></>);
  const formatCmd = (code) => code.join("\n");

  return (
    <div class="card" style={{marginBottom: "30px"}}>
      <div class="card-body" style={{paddingRight: "45px"}}>
        <pre class="card-text" style={{whiteSpace: "pre-wrap"}}>
          {formatCode(code)}
        </pre>
      </div>
      <div
        style={{
          position: 'absolute',
          right: '5px',
          top: '5px',
        }}
      >
        {showCopyIcon &&
          <CopyToClipboard text={formatCmd(code)} onCopy={handleCopyToClipboard} data-tip data-for="copiedtip" style={{width:"auto", padding:"0.2rem 0.4rem"}}>
            <button type="button" className="btn btn-outline-secondary">
              <FontAwesomeIcon icon={faCopy} color="dimgray" size="md"/>
            </button>
          </CopyToClipboard>
        }
        {showCheckIcon &&
          <button disabled type="button" className="btn btn-outline-secondary" style={{width:"auto", padding:"0.2rem 0.4rem"}}>
            <FontAwesomeIcon icon={faCheck} color="dimgray" size="md"/>
          </button>
        }
      </div>
    </div>
  );
};

export default CodeSnippet;

import React, { useState } from "react";
import * as ReactDOM from "react-dom";
import PropTypes from "prop-types";

const DownloadModalWindowElement = (props) => {
  const { authorized, imagePath, ...element } = props;

  const close = (event) => {
    $("#downloadModal").modal("hide");
  };

  return ReactDOM.createPortal(
    <div className="modal-content">
      <div className="modal-body">
        <table>
         <tr>
           <td style={{width:"150px"}}>
             <img src="static/img/conp.png" className="text-center" style={{width:"100%"}}/>
           </td>
           <td style={{width:"25px"}}></td>
           <td colSpan="41">
             <h4 className="modal-title w-100 text-center" id="modalLongTitle">
               You are about to download a {element.size} file.
             </h4>
             <h4 className="modal-title w-100 text-center" id="modalLongTitle">Are you sure?</h4>
           </td>
         </tr>
       </table>
      </div>
      <div className="modal-footer">
       <div className="btn-group btn-group-lg" style={{width:"100%"}}>
         <button
           type="button"
           className="btn btn-outline-secondary"
           data-dismiss="modal"
           id="cancelDownload"
         >
           Cancel
         </button>
         <a
           href={ element.zipLocation }
           className="btn btn-secondary"
           id="confirmDownload"
           onClick={close}
         >
           Download
         </a>
       </div>
     </div>
    </div>,
    document.querySelector("#downloadModalDocument")
  );
};

DownloadModalWindowElement.propTypes = {
  authorized: PropTypes.bool,
  onRunWithCBRAIN: PropTypes.func,
  // element proptypes
  id: PropTypes.string,
  title: PropTypes.string,
  isPrivate: PropTypes.bool,
  thumbnailURL: PropTypes.string,
  imagePath: PropTypes.string,
  downloadPath: PropTypes.string,
  downloads: PropTypes.number,
  views: PropTypes.number,
  likes: PropTypes.number,
  dateAdded: PropTypes.string,
  dateUpdated: PropTypes.string,
  size: PropTypes.string,
  files: PropTypes.number,
  subjects: PropTypes.number,
  formats: PropTypes.string,
  modalities: PropTypes.string,
  sources: PropTypes.number,
  cbrain_id: PropTypes.string,
  ark_id: PropTypes.string,
  zipLocation: PropTypes.string,
  showDownloadButton: PropTypes.bool,
};

DownloadModalWindowElement.defaultProps = {
  imagePath: "",
  downloadPath: "",
}

export default DownloadModalWindowElement;

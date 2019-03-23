import React from "react";
import PropTypes from "prop-types";

const DataTable = ({
  authorized,
  elements,
  query,
  setQuery,
  onDownload,
  onRunWithCBRAIN,
  imgPath
}) => {
  const runOnCbrainEnabled = `${imgPath}/run_on_cbrain_green.png`;
  const runOnCbrainDisabled = `${imgPath}/run_on_cbrain_gray.png`;
  const downloadEnabled = `${imgPath}/download_green.png`;
  const downloadDisabled = `${imgPath}/download_gray.png`;

  return (
    <div className="search-dataset-table" cellSpacing={0}>
      <div className="search-dataset-toolbar">SEARCH TOOLBAR</div>
      {elements.map(element => {
        return (
          <div className="search-dataset">
            <div className="dataset-social">
              <img
                alt="dataset format"
                className="dataset-social-img"
                src={element.thumbnailURL}
              />
              <div className="dataset-social-icons">
                <div className="dataset-social-icon">
                  <i className="fa fa-download social-fa" />
                  <div>{element.downloads}</div>
                </div>
                <div className="dataset-social-icon">
                  <i className="fa fa-eye social-fa" />
                  <div>{element.views}</div>
                </div>
                <div className="dataset-social-icon">
                  <i className="fa fa-heart social-fa" />
                  <div>{element.likes}</div>
                </div>
              </div>
            </div>
            <div className="dataset-details">
              <div className="dataset-details-stats">
                <div className="dataset-title">
                  <div>{element.title}</div>
                </div>
                <div className="dataset-stat">
                  <div className="dataset-stat-text">Date Added</div>
                  <div className="dataset-stat-num">{element.dateAdded}</div>
                </div>
                <div className="dataset-stat">
                  <div className="dataset-stat-text">Date Updated</div>
                  <div className="dataset-stat-num">{element.dateUpdated}</div>
                </div>
                <div className="dataset-stat">
                  <div className="dataset-stat-text">Size</div>
                  <div className="dataset-stat-num">{element.size}</div>
                </div>
                <div className="dataset-stat">
                  <div className="dataset-stat-text">Files</div>
                  <div className="dataset-stat-num">{element.files}</div>
                </div>
                <div className="dataset-stat">
                  <div className="dataset-stat-text">Subjects</div>
                  <div className="dataset-stat-num">{element.subjects}</div>
                </div>
                <div className="dataset-stat">
                  <div className="dataset-stat-text">Format</div>
                  <div className="dataset-stat-num">{element.format}</div>
                </div>
                <div className="dataset-stat">
                  <div className="dataset-stat-text">Modalities</div>
                  <div className="dataset-stat-num">{element.modalities}</div>
                </div>
                <div className="dataset-stat">
                  <div className="dataset-stat-text">Sources</div>
                  <div className="dataset-stat-num">{element.sources}</div>
                </div>
              </div>
              <div className="dataset-options">
                <div className="dataset-option">
                  <img
                    alt="Run On Cbrain"
                    className="run-on-cbrain-button option-icon"
                    src={
                      element.public || authorized
                        ? runOnCbrainEnabled
                        : runOnCbrainDisabled
                    }
                    onClick={event => {
                      event.preventDefault();
                      if (!(element.public || authorized)) {
                        return;
                      }
                      onRunWithCBRAIN instanceof Function &&
                        onRunWithCBRAIN(event);
                    }}
                  />
                </div>
                <div className="dataset-option">
                  <img
                    alt="Run On Cbrain"
                    className="download-button  option-icon"
                    src={
                      element.public || authorized
                        ? downloadEnabled
                        : downloadDisabled
                    }
                    onClick={event => {
                      event.preventDefault();
                      if (!(element.public || authorized)) {
                        return;
                      }
                      onDownload instanceof Function && onDownload(event);
                    }}
                  />
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

DataTable.propTypes = {
  authorized: PropTypes.bool,
  elements: PropTypes.arrayOf(
    PropTypes.shape({
      public: PropTypes.bool,
      thumbnailURL: PropTypes.string,
      downloads: PropTypes.number,
      views: PropTypes.number,
      likes: PropTypes.number,
      dateAdded: PropTypes.string,
      dateUpdated: PropTypes.string,
      size: PropTypes.string,
      files: PropTypes.number,
      subjects: PropTypes.number,
      format: PropTypes.string,
      modalities: PropTypes.string,
      sources: PropTypes.number
    })
  ),
  query: PropTypes.shape({
    sort: PropTypes.shape({
      key: PropTypes.string,
      comparitor: PropTypes.string
    }),
    page: PropTypes.number,
    search: PropTypes.string
  }),
  setQuery: PropTypes.func,
  onDownload: PropTypes.func,
  onRunWithCBRAIN: PropTypes.func
};

DataTable.defaultProps = {
  imgPath: ""
};

export default DataTable;

// import React from "react";
// import PropTypes from "prop-types";

// const DataTable = ({
//   authorized,
//   elements,
//   query,
//   setQuery,
//   onDownload,
//   onRunWithCBRAIN,
//   imgPath
// }) => {
//   const runOnCbrainEnabled = `${imgPath}/run_on_cbrain_green.png`;
//   const runOnCbrainDisabled = `${imgPath}/run_on_cbrain_gray.png`;
//   const downloadEnabled = `${imgPath}/download_green.png`;
//   const downloadDisabled = `${imgPath}/download_gray.png`;

//   return (
//     <table className="table data-table row-border" cellSpacing={0}>
//       <thead />
//       <tbody>
//         {elements.map(element => {
//           return (
//             <tr>
//               <td>
//                 <table className="table">
//                   <tbody>
//                     <tr>
//                       <th colSpan={3}>
//                         <img
//                           alt="dataset format"
//                           className="dataset-thumbnail"
//                           src={element.thumbnailURL}
//                         />
//                       </th>
//                     </tr>
//                     <tr>
//                       <td>
//                         <i className="fa fa-download" />
//                       </td>
//                       <td>
//                         <i className="fa fa-eye" />
//                       </td>
//                       <td>
//                         <i className="fa fa-heart" />
//                       </td>
//                     </tr>
//                     <tr>
//                       <td>{element.downloads}</td>
//                       <td>{element.views}</td>
//                       <td>{element.likes}</td>
//                     </tr>
//                   </tbody>
//                 </table>
//               </td>
//               <td>
//                 <table className="table">
//                   <tbody>
//                     <tr>
//                       <th colSpan={8}>
//                         <h3>{element.title}</h3>
//                       </th>
//                     </tr>
//                     <tr>
//                       <td>Date Added</td>
//                       <td>Date Updated</td>
//                       <td>Size</td>
//                       <td>Files</td>
//                       <td>Subjects</td>
//                       <td>Format</td>
//                       <td>Modalities</td>
//                       <td>Sources</td>
//                     </tr>
//                     <tr>
//                       <td>{element.dateAdded}</td>
//                       <td>{element.dateUpdated}</td>
//                       <td>{element.size}</td>
//                       <td>{element.files}</td>
//                       <td>{element.subjects}</td>
//                       <td>{element.format}</td>
//                       <td>{element.modalities}</td>
//                       <td>{element.sources}</td>
//                     </tr>
//                   </tbody>
//                 </table>
//               </td>
//               <td>
//                 <img
//                   alt="Run On Cbrain"
//                   className="run-on-cbrain-button"
//                   src={
//                     element.public || authorized
//                       ? runOnCbrainEnabled
//                       : runOnCbrainDisabled
//                   }
//                   onClick={event => {
//                     event.preventDefault();
//                     if (!(element.public || authorized)) {
//                       return;
//                     }
//                     onRunWithCBRAIN instanceof Function &&
//                       onRunWithCBRAIN(event);
//                   }}
//                 />
//               </td>
//               <td>
//                 <img
//                   alt="Run On Cbrain"
//                   className="download-button"
//                   src={
//                     element.public || authorized
//                       ? downloadEnabled
//                       : downloadDisabled
//                   }
//                   onClick={event => {
//                     event.preventDefault();
//                     if (!(element.public || authorized)) {
//                       return;
//                     }
//                     onDownload instanceof Function && onDownload(event);
//                   }}
//                 />
//               </td>
//             </tr>
//           );
//         })}
//       </tbody>
//       <tfoot />
//     </table>
//   );
// };

// DataTable.propTypes = {
//   authorized: PropTypes.bool,
//   elements: PropTypes.arrayOf(
//     PropTypes.shape({
//       public: PropTypes.bool,
//       thumbnailURL: PropTypes.string,
//       downloads: PropTypes.number,
//       views: PropTypes.number,
//       likes: PropTypes.number,
//       dateAdded: PropTypes.string,
//       dateUpdated: PropTypes.string,
//       size: PropTypes.string,
//       files: PropTypes.number,
//       subjects: PropTypes.number,
//       format: PropTypes.string,
//       modalities: PropTypes.string,
//       sources: PropTypes.number
//     })
//   ),
//   query: PropTypes.shape({
//     sort: PropTypes.shape({
//       key: PropTypes.string,
//       comparitor: PropTypes.string
//     }),
//     page: PropTypes.number,
//     search: PropTypes.string
//   }),
//   setQuery: PropTypes.func,
//   onDownload: PropTypes.func,
//   onRunWithCBRAIN: PropTypes.func
// };

// DataTable.defaultProps = {
//   imgPath: ""
// };

// export default DataTable;

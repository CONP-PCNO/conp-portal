import React, { Component } from "react";
import { render } from "react-dom";

import { DataTable } from "../../src";

const authorized = true;

const exampleList = [
  {
    thumbnailURL: "",
    downloads: 42,
    views: 24,
    likes: 12,
    dateAdded: "10/12/2018",
    dateUpdated: "10/13/2018",
    size: "800mb",
    files: 44,
    subjects: 30,
    format: "BIDS",
    modalities: "fMRI",
    sources: 3
  }
];

class Demo extends Component {
  render() {
    return (
      <div>
        <h1>conp-search Demo</h1>
        <DataTable authorized={authorized} elements={exampleList} />
      </div>
    );
  }
}

render(<Demo />, document.querySelector("#demo"));

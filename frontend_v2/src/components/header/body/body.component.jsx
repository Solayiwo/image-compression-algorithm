import React from "react";
import './body.styles.scss';

const Body = () => (
    <div className="body">
        <div className="text">
            <h2>Image Compressor</h2>
            <span>Compress your images optimally</span>
        </div>
        <div className="work-area">
            <button>Upload File</button>
            <div className="drop-file">Drop your files here</div>
        </div>
    </div>
);

export default Body;
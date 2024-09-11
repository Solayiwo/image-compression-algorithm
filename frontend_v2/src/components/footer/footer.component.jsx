import React from "react";
import { Link } from "react-router-dom";
import './footer.styles.scss';
import Twitter from './images/twitter_3148434.png'

const Footer = () => (
    <div className="footer">
        <h3>Image Compressor tool</h3>
        <div className="nav-list">
            <div className="options">
                <Link className="option" to='/api'>
                    API
                </Link>
                <Link className="option" to='/about'>
                    ABOUT US
                </Link>
                <Link className="option" to='/signin'>
                    SIGNIN
                </Link>
            </div>
        </div>
        <div className="design"></div>

        <div className="icons">
            {/* <img className='twitter' src={Twitter} alt="Twitter" />             */}
        </div>

        <span>@Copyright2024, All Rights Reserved</span>
    </div>
);

export default Footer;
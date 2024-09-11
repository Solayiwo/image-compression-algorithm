import React from 'react';
import { Link } from 'react-router-dom';
import './header.styles.scss';
import Logo from './images/Logo.png';

const Header = () => (
    <div className="header">
        <Link to='/' className="logo-container">
            {/* <Logo className="logo" /> */}
            <img className='logo' src={Logo} alt="Logo" />
        </Link>
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
);

export default Header;
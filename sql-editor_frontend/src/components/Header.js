import React from 'react';
import { Link } from 'react-router-dom';
import '../Styles/Navbar.css'
import '../Styles/Header.css'
function Header() {
  return (
    <header>
      <div className="container-fluid">
          {/* Brand Link */}
          <Link className="navbar-brand" to="/">SQL Practice Tool</Link>
      </div>
    </header>
  );
}

export default Header;
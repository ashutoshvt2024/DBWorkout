import React from 'react';
import '../Styles/Footer.css'
function Footer() {
  return (
    <footer className="bg-dark text-light py-3 mt-auto">
      <div className="container text-center">
        <p>&copy; 2024 SQL Practice Tool. All rights reserved.</p>
        <p>
          <a href="/terms" className="text-light">Terms of Service</a> | <a href="/privacy" className="text-light">Privacy Policy</a>
        </p>
      </div>
    </footer>
  );
}

export default Footer;
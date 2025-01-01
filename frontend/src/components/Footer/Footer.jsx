import React from "react";
import "./Footer.css";
import {FaFacebookF, FaInstagram, FaTwitter, FaYoutube,FaDiscord} from "react-icons/fa";

const Footer = () => {
    return (
        <footer className="footer bg-dark text-white py-6" id="footer">
            <div className="container">
                <div className="footer-content text-center">
                    <div className="footer-item-group grid">
                        <div className="footer-item">
                            <h3 className="footer-item footer-title text-upper">GameTech</h3>
                            <ul className="footer-item footer-links">
                                <li><a href="#">The Company</a></li>
                                <li><a href="#">History</a></li>
                                <li><a href="#">Contact Us</a></li>
                            </ul>
                        </div>
                        <div className="footer-item">
                        <h3 className="footer-title text-upper">GameTech</h3>
                        <ul className="footer-links">

                                <li><a href="#">SearcGame and Price</a></li>
                                <li><a href="#">Basic Info</a></li>
                                <li><a href="#">Contact Form</a></li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div className="footer-social-icons flex flex-center">
                    <a href="https://www.facebook.com/" className="bg-red flex flex-center" aria-label="Facebook"><FaFacebookF /></a>
                    <a href="https://www.instagram.com/" className="bg-red flex flex-center" aria-label="Instagram"><FaInstagram /></a>
                    <a href="https://www.twitter.com/" className="bg-red flex flex-center" aria-label="Twitter"><FaTwitter /></a>
                    <a href="https://www.youtube.com/" className="bg-red flex flex-center" aria-label="YouTube"><FaYoutube /></a>
                    <a href="https://www.discord.com/" className="bg-red flex flex-center" aria-label="Discord"><FaDiscord /></a>

                </div>

                <div className="footer-bottom-text">
                    <p className="text fs-16">Copyright © 2024 GameTech. All rights reserved.</p>
                </div>
            </div>
        </footer>
    )
}
export default Footer;
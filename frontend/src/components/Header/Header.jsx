import React from "react";
import images from "../../constants/images";
import "./Header.css";
import { FaPaperPlane } from "react-icons/fa";
import Navbar from "./Navbar/Navbar";

const Header = () => {
    return (
        <header className="header flex" id="header">
            <Navbar />
            <div className="container">
                <div className="header-content grid text-center py-6 text-white">
                    {/* Left Content */}
                    <div className="header-content-left" data-aos="fade-right">
                        <h1 className="text-upper header-tittle">SEARCHGAME APP DEVELOPMENT</h1>
                        <p className="text">
                        Welcome to the ultimate game price comparison platform! Whether you’re a fan of Epic Games, a loyal Steam user, or love the DRM-free gaming experience of GOG, we’ve got you covered. Our mission is simple – to help you find the best deals for your favorite games across these major gaming platforms.

Gaming can be expensive, but it doesn’t have to be. With our powerful search engine, you can quickly compare prices for thousands of games, ensuring you never overpay again. From the latest blockbusters to indie gems, our platform makes it easy to discover where your favorite games are being sold at the lowest price.

No more jumping from platform to platform or waiting for sales to stumble upon. Our system fetches real-time data from Epic Games, Steam, and GOG, providing you with up-to-date information about discounts, bundles, and exclusive deals. Whether it’s Cyberpunk 2077, GTA 5, or a classic RPG, you’ll always find the best price here
                        </p>
                        <a href="#" className="btn btn-dark">
                            <span>View More</span> <FaPaperPlane />
                        </a>
                    </div>
                    
                    {/* Right Content */}
                    <div className="header-content-right" data-aos="fade-left">
                        <img src={images.redconsol2} alt="redconsol2" className="header-images" />
                    </div>
                </div>

                
            </div>
        </header>
    );
};

export default Header;
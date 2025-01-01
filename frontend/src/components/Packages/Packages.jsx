import React from 'react';
import data from "../../constants/data";
import "./Packages.css";

const Packages = () => {
    return (
        <section className="package-content py-6" id="packages">
            <div className="container">
                <div className="section-title bg-dark">
                    <h2 className="text-upper text-white text-center">Our Packages</h2>
                </div>
                <div className="packages-content" grid py-6>
                    {
                        data.packages.map((packg, index) => {
                            return (
                            <div className="package-item text-center mx-auto" key={index} data-aos = "fade-up" data-aos-duration = "3000">
                                <h3 className="package-item-title">{packg.type}</h3>
                                <ul className="package-item-list">
                                    {
                                        packg.service_list.map((service, idx) => {
                                            return (
                                                <li key = {idx}>{service}</li>
                                            )
                                        })
                                    }
                                </ul>
                                <div className="packages-item-price">
                                    <span>${packg.price}</span> /mo.
                                </div>
                                <a href = "#" className="btn btn-red">Order Now</a>
                            </div>
                            )
                        })
                    }
                </div>
            </div>
        </section>
    );
};

export default Packages;
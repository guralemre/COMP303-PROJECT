import React from "react";
import images from "../../constants/images";
import { what_we_do } from "../../constants/data"; // Doğru şekilde import
import "./WhatWeDo.css";

const WhatWeDo = () => {
    return (
        <section className="what-we-do py-6" id="what-we-do">
            <div className="container">
                <div className="section-title bg-dark">
                    <h2 className="text-upper text-white text-center">
                        What We Do
                    </h2>
                </div>

                <div className="what-we-do-content">
                    {
                        what_we_do.map((whatItem, index) => ( // Burada data değil, what_we_do kullanılıyor
                            <div className="what-we-do-item grid text-center" key={index}>
                                <div className="what-we-do-item-left" data-aos = "fade-right">
                                    <img
                                        src={whatItem.image} // `slider4` doğruysa kullanılır
                                        alt=""
                                        className="mx-auto"
                                    />
                                </div>
                                <div className="what-we-do-item-right" data-aos = "fade-left">
                                    <h4 className="text-upper fs-20">
                                        {whatItem.title}
                                    </h4>
                                    <p className="text mx-auto">
                                        {whatItem.paragraph}
                                    </p>
                                    <a href="#" className="btn btn-red">
                                        View More
                                    </a>
                                </div>
                            </div>
                        ))
                    }
                </div>
            </div>
        </section>
    );
};

export default WhatWeDo;

import React from 'react';
import data from "../../constants/data";
import "./Projects.css";

const Projects = () => {
    return (
        <section className="projects py-6" id="projects">
            <div className="container">
                <div className="section-title bg-dark">
                    <h2 className="text-upper text-white text-center">Our Projects</h2>
                </div>

                {/* YouTube Video */}
                <div className="video-wrapper text-center">
                    <iframe
                        className="projects-video"
                        src="https://www.youtube.com/embed/QdBZY2fkU-0?autoplay=1&mute=1&loop=1&playlist=QdBZY2fkU-0"
                        title="YouTube Video"
                        frameBorder="0"
                        allow="autoplay; fullscreen"
                        allowFullScreen
                    ></iframe>
                </div>

                <div className="projects-content grid py-6">
                    {
                        data.projects.map((project, index) => {
                            return (
                                <div
                                    className="projects-item text-center"
                                    key={index}
                                    data-aos="zoom-in"
                                >
                                    <img
                                        src={project.image}
                                        alt={project.title}
                                        className="mx-auto"
                                    />
                                    <h4 className="text-upper">{project.title}</h4>
                                </div>
                            );
                        })
                    }
                </div>
            </div>
        </section>
    );
};

export default Projects;

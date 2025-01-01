import React from "react";
import "./Team.css";
import data from "../../constants/data";

const Team = () => {
    return (
        <section className="team py-6 bg-red" id="team">
            <div className="container">
                <div className="section-title bg-dark">
                    <h2 className="text-upper text-white text-center">Our Team</h2>
                </div>
                <div className="team-content py-6 grid">
                    {
                        data.teams.map((team, index) => {
                            return (
                                <div className="team-item text-center text-white" key={index} data-aos = "fade-up">
                                    <img src={team.image} alt="team_image" 
                                    className="mx-auto" />
                                    <p className="text-upper fw-7">{team.name}</p>
                                    <span className="text-upper">{team.post}</span>
                                </div>
                            )
                        })
                    }
                </div>
            </div>
        </section>
    )
};

export default Team;
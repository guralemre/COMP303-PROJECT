import React from "react";
import "./Support.css";
import image from "../../constants/images";

const Support = () => {
    return (
        <section className="support py-6" id="support">
            <div className="container">
                <div className="section-title bg-dark">
                    <h2 className="text-upper text-white text-center">Updates & support</h2>
                </div>
                <div className="support-content grid py-6 text-center">
                    <div className="support-content-left" data-aos = "fade-right">
                    <p className="text mx-auto">
  We are Here to Make Your Gaming Experience Seamless!
  Have questions or need assistance? Whether you are facing an issue with game prices, platform details, or any other concern, our support team is ready to help.
  Your Questions Answered Instantly
  Check our FAQs or contact us directly for personalized assistance. We are here 24/7 to ensure you have the best experience.
  Quick and Reliable Support for Gamers
  Our goal is to make sure you get the help you need as quickly as possible. Explore our support options below and reach out to us anytime.
</p>

                        <div className="text mx-auto">
  <h4>Frequently Asked Questions (FAQs):</h4>
  <p>• How do I search for game prices?</p>
  <p>• What platforms are supported?</p>
  <p>• How often are prices updated?</p>
  
  <h4>Live Chat:</h4>
  <p>Need immediate help? Chat with our support team now!</p>
  
  <h4>Email Support:</h4>
  <p>Prefer email? Send us a message at <a href="mailto:support@example.com">support@example.com</a>, and we’ll get back to you within 24 hours.</p>
  
  <h4>Community Support:</h4>
  <p>Join our community forum to discuss and solve issues with fellow gamers.</p>
</div>

                        <a href="#" className="btn btn-red">Support Center</a>
                    </div>
                    <div className="support-content-right" data-aos = "fade-left">
                        <img src={image.support1} alt="support_image"
                        className="mx-auto" />
                    </div>
                </div>
            </div>
        </section>
    )
};
export default Support;
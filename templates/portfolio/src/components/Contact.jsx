import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Mail, Linkedin, Github, Send, MapPin, Phone } from 'lucide-react';

const Contact = ({ contact }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission
    console.log('Form submitted:', formData);
    alert('Thank you for your message! I will get back to you soon.');
    setFormData({ name: '', email: '', message: '' });
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <section id="contact" className="py-20 bg-dark-200">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-center">
            Get In <span className="gradient-text">Touch</span>
          </h2>
          
          <p className="text-gray-400 text-center mb-12 max-w-2xl mx-auto">
            Have a project in mind or want to discuss opportunities? 
            I'd love to hear from you!
          </p>

          <div className="grid md:grid-cols-2 gap-12 max-w-4xl mx-auto">
            {/* Contact Info */}
            <div>
              <h3 className="text-xl font-semibold mb-6">Contact Information</h3>
              
              <div className="space-y-4">
                <a
                  href={`mailto:${contact?.email || ''}`}
                  className="flex items-center gap-4 p-4 card hover:border-primary-500"
                >
                  <div className="w-10 h-10 rounded-lg bg-primary-500/20 flex items-center justify-center">
                    <Mail className="text-primary-500" size={20} />
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Email</p>
                    <p className="text-white">{contact?.email || 'email@example.com'}</p>
                  </div>
                </a>

                <a
                  href={contact?.linkedin || '#'}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-4 p-4 card hover:border-primary-500"
                >
                  <div className="w-10 h-10 rounded-lg bg-primary-500/20 flex items-center justify-center">
                    <Linkedin className="text-primary-500" size={20} />
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">LinkedIn</p>
                    <p className="text-white">Connect on LinkedIn</p>
                  </div>
                </a>

                <a
                  href={contact?.github || '#'}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-4 p-4 card hover:border-primary-500"
                >
                  <div className="w-10 h-10 rounded-lg bg-primary-500/20 flex items-center justify-center">
                    <Github className="text-primary-500" size={20} />
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">GitHub</p>
                    <p className="text-white">View my code</p>
                  </div>
                </a>
              </div>
            </div>

            {/* Contact Form */}
            <div>
              <h3 className="text-xl font-semibold mb-6">Send a Message</h3>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <input
                    type="text"
                    name="name"
                    placeholder="Your Name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 bg-dark-100 border border-gray-700 rounded-lg focus:border-primary-500 focus:outline-none text-white"
                  />
                </div>
                
                <div>
                  <input
                    type="email"
                    name="email"
                    placeholder="Your Email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 bg-dark-100 border border-gray-700 rounded-lg focus:border-primary-500 focus:outline-none text-white"
                  />
                </div>
                
                <div>
                  <textarea
                    name="message"
                    placeholder="Your Message"
                    rows="5"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 bg-dark-100 border border-gray-700 rounded-lg focus:border-primary-500 focus:outline-none text-white resize-none"
                  />
                </div>
                
                <button type="submit" className="btn-primary w-full flex items-center justify-center gap-2">
                  <Send size={18} />
                  Send Message
                </button>
              </form>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Contact;

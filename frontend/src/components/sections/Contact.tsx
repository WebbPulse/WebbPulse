import React from 'react';
import { Button } from '../common';
import type { BaseComponentProps } from '../../types';

export type ContactProps = BaseComponentProps;

export const Contact: React.FC<ContactProps> = ({ className = '' }) => {
  return (
    <section
      id="contact"
      className={`py-20 bg-white dark:bg-gray-900 ${className}`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Get In Touch
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Ready to start a project or just want to chat? I'd love to hear from
            you!
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Contact Information */}
          <div className="space-y-8">
            <div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                Let's Connect
              </h3>
              <p className="text-lg text-gray-600 dark:text-gray-300 leading-relaxed mb-8">
                I'm always open to discussing interesting projects, or just
                having a chat about software engineering, networking, or
                infrastructure.
              </p>
            </div>

            {/* Contact Methods */}
            <div className="space-y-6">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                  <span className="text-xl">📧</span>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 dark:text-white">
                    Email
                  </h4>
                  <p className="text-gray-600 dark:text-gray-300">
                    tyler@webbpulse.com
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
                  <span className="text-xl">💼</span>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 dark:text-white">
                    LinkedIn
                  </h4>
                  <p className="text-gray-600 dark:text-gray-300">
                    linkedin.com/in/tylert2610
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center">
                  <span className="text-xl">🐙</span>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 dark:text-white">
                    GitHub
                  </h4>
                  <p className="text-gray-600 dark:text-gray-300">
                    github.com/Tylert2610
                  </p>
                </div>
              </div>
            </div>

            {/* Availability */}
            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
              <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                Current Availability
              </h4>
              <p className="text-gray-600 dark:text-gray-300">
                Currently a software engineer at Verkada. Always happy to chat
                about software, networking, or interesting side projects.
              </p>
            </div>
          </div>

          {/* Contact Form Placeholder */}
          <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-8">
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
              Send a Message
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              Contact form integration will be implemented in Phase 4. For now,
              feel free to reach out via email or LinkedIn!
            </p>

            {/* Placeholder Form */}
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Name
                </label>
                <input
                  type="text"
                  disabled
                  placeholder="Your name"
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  disabled
                  placeholder="your.email@example.com"
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Message
                </label>
                <textarea
                  disabled
                  rows={4}
                  placeholder="Your message..."
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed resize-none"
                />
              </div>

              <Button variant="primary" disabled className="w-full">
                Contact Form Coming Soon
              </Button>
            </div>
          </div>
        </div>

        {/* Quick Contact Buttons */}
        <div className="mt-16 text-center">
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              variant="primary"
              size="lg"
              onClick={() =>
                window.open('mailto:tyler@webbpulse.com', '_blank')
              }
            >
              Send Email
            </Button>
            <Button
              variant="outline"
              size="lg"
              onClick={() =>
                window.open('https://www.linkedin.com/in/tylert2610/', '_blank')
              }
            >
              Connect on LinkedIn
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

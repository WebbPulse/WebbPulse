import React from 'react';
import { Button } from '../common';

interface HeroProps {
  title?: string;
  subtitle?: string;
  description?: string;
  ctaText?: string;
  ctaLink?: string;
}

const Hero: React.FC<HeroProps> = ({
  title = "Hi, I'm Tyler Webb",
  subtitle = 'Software Engineer',
  description = 'Software engineer at Verkada, building privacy-conscious physical security software. Background in network engineering and full-stack web.',
  ctaText = 'View My Work',
  ctaLink = '#projects',
}) => {
  return (
    <section className="bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 py-20 lg:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
            {title}
          </h1>
          <h2 className="text-xl md:text-2xl text-blue-600 dark:text-blue-400 mb-8">
            {subtitle}
          </h2>
          <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto mb-12 leading-relaxed">
            {description}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              variant="primary"
              size="lg"
              onClick={() => {
                const element = document.querySelector(ctaLink);
                element?.scrollIntoView({ behavior: 'smooth' });
              }}
            >
              {ctaText}
            </Button>
            <Button
              variant="outline"
              size="lg"
              onClick={() => {
                const element = document.querySelector('#contact');
                element?.scrollIntoView({ behavior: 'smooth' });
              }}
            >
              Get In Touch
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;

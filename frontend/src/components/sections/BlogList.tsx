import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Header, Footer } from '../layout';
import { Card, Button } from '../common';
import { apiService } from '../../services/api';
import type { BlogPost } from '../../services/api';
import type { NavigationItem, SocialLink } from '../../types';

export const BlogList: React.FC = () => {
  const [blogPosts, setBlogPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [categories, setCategories] = useState<
    { id: number; name: string; slug: string }[]
  >([]);

  const navigationItems: NavigationItem[] = [
    { label: 'Home', href: '/' },
    { label: 'About', href: '/#about' },
    { label: 'Skills', href: '/#skills' },
    { label: 'Projects', href: '/#projects' },
    { label: 'Experience', href: '/#experience' },
    { label: 'Blog', href: '/blog' },
    { label: 'Contact', href: '/#contact' },
  ];

  const socialLinks: SocialLink[] = [
    {
      platform: 'GitHub',
      url: 'https://github.com/Tylert2610',
      icon: 'github',
    },
    {
      platform: 'LinkedIn',
      url: 'https://www.linkedin.com/in/tylert2610/',
      icon: 'linkedin',
    },
  ];

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const [postsResponse, categoriesResponse] = await Promise.all([
          apiService.getBlogPosts(),
          apiService.getCategories(),
        ]);

        if (postsResponse.error) {
          setError(postsResponse.error);
        } else {
          setBlogPosts(postsResponse.data || []);
        }

        if (categoriesResponse.error) {
          console.error('Failed to load categories:', categoriesResponse.error);
        } else {
          setCategories(categoriesResponse.data || []);
        }
      } catch {
        setError('Failed to load blog posts');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const filteredPosts = selectedCategory
    ? blogPosts.filter(post => post.category?.slug === selectedCategory)
    : blogPosts;

  const publishedPosts = filteredPosts.filter(post => post.published_at);

  if (loading) {
    return (
      <div className="min-h-screen bg-white dark:bg-gray-900">
        <Header navigationItems={navigationItems} />
        <main className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-600 dark:text-gray-300">
              Loading blog posts...
            </p>
          </div>
        </main>
        <Footer socialLinks={socialLinks} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-white dark:bg-gray-900">
        <Header navigationItems={navigationItems} />
        <main className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              Error Loading Blog Posts
            </h1>
            <p className="text-gray-600 dark:text-gray-300 mb-6">{error}</p>
            <Button variant="outline" onClick={() => window.location.reload()}>
              Try Again
            </Button>
          </div>
        </main>
        <Footer socialLinks={socialLinks} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900">
      <Header navigationItems={navigationItems} />
      <main className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Blog & Articles
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Thoughts on web development, technology trends, and best practices
            </p>
          </div>

          {/* Category Filter */}
          {categories.length > 0 && (
            <div className="mb-12">
              <div className="flex flex-wrap justify-center gap-4">
                <button
                  onClick={() => setSelectedCategory(null)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                    selectedCategory === null
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                  }`}
                >
                  All Posts
                </button>
                {categories.map(category => (
                  <button
                    key={category.id}
                    onClick={() => setSelectedCategory(category.slug)}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                      selectedCategory === category.slug
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                    }`}
                  >
                    {category.name}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Blog Posts Grid */}
          {publishedPosts.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {publishedPosts.map(post => (
                <BlogPostCard key={post.id} post={post} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                {selectedCategory
                  ? `No blog posts found in the "${categories.find(c => c.slug === selectedCategory)?.name}" category.`
                  : 'No blog posts available yet. Check back soon!'}
              </p>
              {selectedCategory && (
                <Button
                  variant="outline"
                  onClick={() => setSelectedCategory(null)}
                >
                  View All Posts
                </Button>
              )}
            </div>
          )}

          {/* Back to Home */}
          <div className="text-center mt-16">
            <Link to="/">
              <Button variant="outline">← Back to Home</Button>
            </Link>
          </div>

        </div>
      </main>
      <Footer socialLinks={socialLinks} />
    </div>
  );
};

const BlogPostCard: React.FC<{ post: BlogPost }> = ({ post }) => {
  return (
    <Card
      title={post.title}
      description={post.excerpt || ''}
      image=""
      category={post.category?.name || ''}
      placeholderType="blog"
      className="h-full hover:shadow-lg transition-shadow duration-300"
    >
      <div className="space-y-4">
        <div className="flex items-center justify-between text-sm">
          {post.category && (
            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-full">
              {post.category.name}
            </span>
          )}
          {post.read_time && (
            <span className="text-gray-500 dark:text-gray-400">
              {post.read_time}
            </span>
          )}
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {post.published_at &&
              new Date(post.published_at).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
              })}
          </span>
          <Link to={`/blog/${post.slug}`}>
            <Button variant="ghost" size="sm">
              Read More →
            </Button>
          </Link>
        </div>
      </div>
    </Card>
  );
};

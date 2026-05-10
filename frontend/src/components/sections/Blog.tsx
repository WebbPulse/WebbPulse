import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Card, Button } from '../common';
import { apiService } from '../../services/api';
import type { BaseComponentProps } from '../../types';
import type { BlogPost } from '../../services/api';

export type BlogProps = BaseComponentProps;

export const Blog: React.FC<BlogProps> = ({ className = '' }) => {
  const [blogPosts, setBlogPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBlogPosts = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await apiService.getBlogPosts();
        if (response.error) {
          setError(response.error);
        } else {
          setBlogPosts(response.data || []);
        }
      } catch {
        setError('Failed to load blog posts');
      } finally {
        setLoading(false);
      }
    };

    fetchBlogPosts();
  }, []);

  // Get featured post (first published post)
  const featuredPost = blogPosts.find(post => post.published_at);

  // Get recent posts (excluding featured)
  const recentPosts = blogPosts
    .filter(post => post.published_at && post.id !== featuredPost?.id)
    .slice(0, 6);

  return (
    <section
      id="blog"
      className={`py-20 bg-gray-50 dark:bg-gray-800 ${className}`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Blog & Articles
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Thoughts on web development, technology trends, and best practices
          </p>
        </div>

        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-600 dark:text-gray-300">
              Loading blog posts...
            </p>
          </div>
        )}

        {error && (
          <div className="text-center py-12">
            <p className="text-red-600 dark:text-red-400 mb-4">{error}</p>
            <Button variant="outline" onClick={() => window.location.reload()}>
              Try Again
            </Button>
          </div>
        )}

        {!loading && !error && (
          <>
            {/* Featured Post */}
            {featuredPost && (
              <div className="mb-16">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-8">
                  Featured Article
                </h3>
                <div className="bg-white dark:bg-gray-700 rounded-lg overflow-hidden shadow-lg">
                  <div className="md:flex">
                    <div className="md:w-1/2">
                      <div className="h-64 md:h-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                        <span className="text-white text-6xl">📝</span>
                      </div>
                    </div>
                    <div className="md:w-1/2 p-8">
                      <div className="flex items-center space-x-4 mb-4">
                        {featuredPost.category && (
                          <span className="px-3 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full">
                            {featuredPost.category.name}
                          </span>
                        )}
                        {featuredPost.read_time && (
                          <span className="text-sm text-gray-500 dark:text-gray-400">
                            {featuredPost.read_time}
                          </span>
                        )}
                      </div>
                      <h4 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                        {featuredPost.title}
                      </h4>
                      {featuredPost.excerpt && (
                        <p className="text-gray-600 dark:text-gray-300 mb-6 leading-relaxed">
                          {featuredPost.excerpt}
                        </p>
                      )}
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-500 dark:text-gray-400">
                          {featuredPost.published_at &&
                            new Date(
                              featuredPost.published_at
                            ).toLocaleDateString('en-US', {
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric',
                            })}
                        </span>
                        <Link to={`/blog/${featuredPost.slug}`}>
                          <Button variant="primary" size="sm">
                            Read More
                          </Button>
                        </Link>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Recent Posts Grid */}
            {recentPosts.length > 0 && (
              <div className="mb-12">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-8">
                  Recent Posts
                </h3>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {recentPosts.map(post => (
                    <BlogPostCard key={post.id} post={post} />
                  ))}
                </div>
              </div>
            )}

            {/* No Posts Message */}
            {blogPosts.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-600 dark:text-gray-300 mb-4">
                  No blog posts available yet. Check back soon!
                </p>
              </div>
            )}
          </>
        )}

        {/* View All Posts Button */}
        {blogPosts.length > 0 && (
          <div className="text-center mt-12">
            <Link to="/blog">
              <Button variant="outline" size="lg">
                View All Posts
              </Button>
            </Link>
          </div>
        )}
      </div>
    </section>
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

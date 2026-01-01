/**
 * Utility functions for formatting data
 */

/**
 * Format price in cents to dollar string
 * @param cents Price in cents
 * @returns Formatted price string (e.g., "$19.99")
 */
export const formatPrice = (cents: number): string => {
  return `$${(cents / 100).toFixed(2)}`;
};

/**
 * Format date to readable string
 * @param dateString ISO 8601 date string
 * @returns Formatted date string
 */
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

/**
 * Format date and time to readable string
 * @param dateString ISO 8601 date string
 * @returns Formatted date and time string
 */
export const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

/**
 * Format timestamp to time string
 * @param dateString ISO 8601 date string
 * @returns Formatted time string
 */
export const formatTime = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  });
};


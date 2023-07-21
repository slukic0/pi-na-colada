// eslint-disable-next-line no-unused-vars
import { act, render, waitFor } from '@testing-library/react';
import axios from 'axios';
import App from '../src/App';
import { describe, expect, it, vi } from 'vitest';

vi.mock('axios');

describe('App', () => {
  it('should match its snapshot', async () => {
    axios.post.mockImplementation((url) => {
      if (url.includes('getDrinksFromIngredients')) {
        return Promise.resolve({
          data: [
            {
              id: 'stefDrink',
              name: "Stef's Drink",
            },
          ],
        });
      }
    });
    axios.get.mockImplementation((url) => {
      if (url.includes('getIngredients')) {
        return Promise.resolve({
          data: {
            id1: { name: 'testName1' },
            id2: { name: 'testName2' },
          },
        });
      }
    });

    let tree;
    await act(async () => {
      tree = render(<App />);
    });
    await waitFor(() => {
      expect(tree).toMatchSnapshot();
    });
  });
});

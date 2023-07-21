import { render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import axios from 'axios';
import { act } from 'react-dom/test-utils';
import ViewDrinks from '../src/components/ViewDrinks';
import UserContextWrapper from './UserContextWrapper';

//import { mock } from '@testing-library/react';

vi.mock('axios');

describe('view ingredient', () => {
  beforeEach(() => {
    axios.post.mockImplementation((url) => {
      if (url.includes('getUserDrinks')) {
        return Promise.resolve({
          data: [
            {
              id: 'testDrinkId',
              mixture: [
                {
                  amount: 1,
                  ingredientId: 'ingId1',
                },
                {
                  amount: 2,
                  ingredientId: 'ingId2',
                },
              ],
              name: 'Test Drink',
            },
          ],
        });
      } else if (url.includes('getIngredient')) {
        return Promise.resolve({
          data: {
            ingId1: { name: 'ingredient1 name' },
            ingId2: { name: 'ingredient2 name' },
          },
        });
      }
    });
  });
  it('should render the table of ingredients', async () => {
    act(() => {
      render(<UserContextWrapper child={<ViewDrinks />} user={{ id: 'userId' }} />);
    });

    await waitFor(() => {
      expect(screen.getByText('Test Drink')).toBeInTheDocument();
      expect(screen.getByText('ingredient1 name, ingredient2 name')).toBeInTheDocument();
    });
  });

  it('should match its snapshot', async () => {
    let tree;
    await act(async () => {
      tree = render(<UserContextWrapper child={<ViewDrinks />} user={{ id: 'userId' }} />);
    });
    await waitFor(() => {
      expect(tree).toMatchSnapshot();
    });
  });
});

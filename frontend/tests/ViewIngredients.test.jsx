import { render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import ViewIngredients from '../src/components/ViewIngredients';
import axios from 'axios';
import { act } from 'react-dom/test-utils';

//import { mock } from '@testing-library/react';

vi.mock('axios');

describe('view ingredient', () => {
  beforeEach(() => {
    axios.get.mockResolvedValue({
      data: {
        id1: { name: 'testName1' },
        id2: { name: 'testName2' },
      },
    });
  });
  it('should render the table of ingredients', async () => {
    act(() => {
      render(<ViewIngredients />);
    });

    await waitFor(() => {
      expect(screen.getByText('testName1')).toBeInTheDocument();
      expect(screen.getByText('testName2')).toBeInTheDocument();
    });
  });

  it('should match its snapshot', async () => {
    let tree;
    await act(async () => {
      tree = render(<ViewIngredients />);
    });
    await waitFor(() => {
      expect(tree).toMatchSnapshot();
    });
  });
});

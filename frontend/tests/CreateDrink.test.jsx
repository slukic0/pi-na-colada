import { render, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import axios from 'axios';
import { act } from 'react-dom/test-utils';
import CreateDrink from '../src/components/CreateDrink';
import UserContextWrapper from './UserContextWrapper';

vi.mock('axios');

describe('create drink', () => {
  beforeEach(() => {
    axios.get.mockResolvedValue({
      data: {
        ingId1: { name: 'ingredient1 name' },
        ingId2: { name: 'ingredient2 name' },
        ingId3: { name: 'ingredient3 name' },
        ingId4: { name: 'ingredient4 name' },
      },
    });
  });
  it('should match its snapshot', async () => {
    let tree;
    await act(async () => {
      tree = render(<UserContextWrapper child={<CreateDrink />} user={{ id: 'userId' }} />);
    });
    await waitFor(() => {
      expect(tree).toMatchSnapshot();
    });
  });
});
